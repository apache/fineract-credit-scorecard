/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.fineract.portfolio.creditscorecard.service;

import java.math.BigDecimal;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.persistence.PersistenceException;
import org.apache.commons.lang3.exception.ExceptionUtils;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.PredictionResponse;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;
import org.apache.fineract.infrastructure.core.api.JsonCommand;
import org.apache.fineract.infrastructure.core.data.CommandProcessingResult;
import org.apache.fineract.infrastructure.core.data.CommandProcessingResultBuilder;
import org.apache.fineract.infrastructure.core.data.EnumOptionData;
import org.apache.fineract.infrastructure.core.exception.PlatformDataIntegrityException;
import org.apache.fineract.infrastructure.security.service.PlatformSecurityContext;
import org.apache.fineract.portfolio.creditscorecard.annotation.ScorecardService;
import org.apache.fineract.portfolio.creditscorecard.domain.CreditScorecard;
import org.apache.fineract.portfolio.creditscorecard.domain.CreditScorecardFeature;
import org.apache.fineract.portfolio.creditscorecard.domain.CreditScorecardFeatureRepository;
import org.apache.fineract.portfolio.creditscorecard.domain.CreditScorecardRepository;
import org.apache.fineract.portfolio.creditscorecard.domain.FeatureConfiguration;
import org.apache.fineract.portfolio.creditscorecard.domain.FeatureCriteria;
import org.apache.fineract.portfolio.creditscorecard.domain.FeatureCriteriaScore;
import org.apache.fineract.portfolio.creditscorecard.domain.MLScorecard;
import org.apache.fineract.portfolio.creditscorecard.domain.MLScorecardFields;
import org.apache.fineract.portfolio.creditscorecard.domain.RuleBasedScorecard;
import org.apache.fineract.portfolio.creditscorecard.domain.StatScorecard;
import org.apache.fineract.portfolio.creditscorecard.exception.FeatureCannotBeDeletedException;
import org.apache.fineract.portfolio.creditscorecard.exception.FeatureNotFoundException;
import org.apache.fineract.portfolio.creditscorecard.serialization.CreditScorecardApiJsonHelper;
import org.apache.fineract.portfolio.loanaccount.domain.Loan;
import org.apache.fineract.portfolio.loanproduct.domain.LoanProduct;
import org.apache.fineract.portfolio.loanproduct.domain.LoanProductRepository;
import org.apache.fineract.portfolio.loanproduct.domain.LoanProductScorecardFeature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.orm.jpa.JpaSystemException;
import org.springframework.transaction.annotation.Transactional;

@PropertySource(value = "classpath:scorecard-client.properties")
@ScorecardService(name = "CreditScorecardWritePlatformService")
public class CreditScorecardWritePlatformServiceImpl implements CreditScorecardWritePlatformService {

    private static final Logger LOG = LoggerFactory.getLogger(CreditScorecardWritePlatformServiceImpl.class);

    @Value("${fineract.credit.scorecard.uid}")
    String username;

    @Value("${fineract.credit.scorecard.password}")
    String password;

    @Value("${fineract.credit.scorecard.baseUrl}")
    String baseUrl;

    private final PlatformSecurityContext context;

    private final LoanProductRepository loanProductRepository;
    private final CreditScorecardApiJsonHelper fromApiJsonDeserializer;
    private final CreditScorecardFeatureRepository featureRepository;
    private final CreditScorecardRepository scorecardRepository;

    AlgorithmsApi scorecardApiClient;

    @Autowired
    public CreditScorecardWritePlatformServiceImpl(final PlatformSecurityContext context,
            final CreditScorecardApiJsonHelper fromApiJsonDeserializer,
            final LoanProductRepository loanProductRepository,
            final CreditScorecardFeatureRepository featureRepository,
            final CreditScorecardRepository scorecardRepository) {
        this.context = context;
        this.fromApiJsonDeserializer = fromApiJsonDeserializer;
        this.loanProductRepository = loanProductRepository;
        this.featureRepository = featureRepository;
        this.scorecardRepository = scorecardRepository;

    }

    private void initScorecardClient() {
        LOG.warn("Base URL at init : {}", baseUrl);
        this.scorecardApiClient = new AlgorithmsApi(Configuration.getDefaultApiClient().setBasePath(baseUrl));
    }

    @Override
    public CommandProcessingResult createScoringFeature(JsonCommand command) {

        try {
            this.context.authenticatedUser();
            this.fromApiJsonDeserializer.validateFeatureForCreate(command.json());

            final CreditScorecardFeature scorecardFeature = CreditScorecardFeature.fromJson(command);
            this.featureRepository.save(scorecardFeature);

            return new CommandProcessingResultBuilder().withCommandId(command.commandId()).withEntityId(scorecardFeature.getId()).build();
        } catch (final JpaSystemException | DataIntegrityViolationException dve) {
            handleDataIntegrityIssues(command, dve.getMostSpecificCause(), dve);
            return CommandProcessingResult.empty();
        } catch (final PersistenceException dve) {
            Throwable throwable = ExceptionUtils.getRootCause(dve.getCause());
            handleDataIntegrityIssues(command, throwable, dve);
            return CommandProcessingResult.empty();
        }
    }

    @Override
    public CommandProcessingResult updateScoringFeature(Long featureId, JsonCommand command) {

        try {
            this.context.authenticatedUser();
            this.fromApiJsonDeserializer.validateFeatureForUpdate(command.json());

            final CreditScorecardFeature featureForUpdate = this.featureRepository.findById(featureId)
                    .orElseThrow(() -> new FeatureNotFoundException(featureId));

            final Map<String, Object> changes = featureForUpdate.update(command);

            if (!changes.isEmpty()) {
                this.featureRepository.save(featureForUpdate);
            }

            return new CommandProcessingResultBuilder().withCommandId(command.commandId()).withEntityId(featureId).with(changes).build();
        } catch (final JpaSystemException | DataIntegrityViolationException dve) {
            handleDataIntegrityIssues(command, dve.getMostSpecificCause(), dve);
            return CommandProcessingResult.empty();
        } catch (final PersistenceException dve) {
            Throwable throwable = ExceptionUtils.getRootCause(dve.getCause());
            handleDataIntegrityIssues(command, throwable, dve);
            return CommandProcessingResult.empty();
        }
    }

    @Transactional
    @Override
    public CreditScorecard assessCreditRisk(final Loan loan) {
        final CreditScorecard scorecard = loan.getScorecard();

        if (scorecard != null) {
            final String scoringMethod = scorecard.getScoringMethod();
            final String scoringModel = scorecard.getScoringModel();

            if (scoringMethod.equalsIgnoreCase("ruleBased")) {

                final RuleBasedScorecard ruleBasedScorecard = scorecard.getRuleBasedScorecard();

                final List<FeatureCriteriaScore> criteriaScores = ruleBasedScorecard.getCriteriaScores();

                for (final FeatureCriteriaScore criteriaScore : criteriaScores) {

                    final LoanProductScorecardFeature lpFeature = criteriaScore.getFeature();

                    final FeatureConfiguration featureConfig = lpFeature.getFeatureConfiguration();

                    final EnumOptionData dataType = lpFeature.getScorecardFeature().getDataType();

                    final List<FeatureCriteria> featureCriteriaList = lpFeature.getFeatureCriteria();

                    for (final FeatureCriteria featureCriteria : featureCriteriaList) {

                        final String value = criteriaScore.getValue();

                        if (value != null) {

                            if (dataType.getValue().equalsIgnoreCase("string")) {

                                if (value.equalsIgnoreCase(featureCriteria.getCriteria())) {
                                    final BigDecimal score = featureCriteria.getScore().multiply(featureConfig.getWeightage());
                                    final String color = featureConfig.getColorFromScore(score);
                                    criteriaScore.setScore(score, color);
                                    break;

                                }

                            } else if (dataType.getValue().equalsIgnoreCase("numeric")) {

                                final String criteria = featureCriteria.getCriteria().strip();

                                final float min = Float.parseFloat(criteria.substring(0, criteria.indexOf("-")).strip());
                                final float max = Float.parseFloat(criteria.substring(criteria.indexOf("-") + 1).strip());

                                final float floatValue = Float.parseFloat(value);

                                if (floatValue >= min && floatValue <= max) {
                                    final BigDecimal score = featureCriteria.getScore().multiply(featureConfig.getWeightage());
                                    final String color = featureConfig.getColorFromScore(score);
                                    criteriaScore.setScore(score, color);
                                    break;

                                }

                            }

                        }

                    }

                }

                BigDecimal scorecardScore = BigDecimal.ZERO;
                int greenCount = 0;
                int amberCount = 0;
                int redCount = 0;
                for (final FeatureCriteriaScore ctScore : criteriaScores) {
                    scorecardScore = scorecardScore.add(ctScore.getScore());

                    if (ctScore.getColor().equalsIgnoreCase("green")) {
                        greenCount += 1;

                    } else if (ctScore.getColor().equalsIgnoreCase("amber")) {
                        amberCount += 1;

                    } else if (ctScore.getColor().equalsIgnoreCase("red")) {
                        redCount += 1;

                    }

                }

                String scorecardColor = "amber";
                if (greenCount > amberCount && greenCount > redCount) {
                    scorecardColor = "green";

                } else if (redCount >= greenCount && redCount >= amberCount) {
                    scorecardColor = "red";

                }

                ruleBasedScorecard.setScore(scorecardScore, scorecardColor);

                return scorecard;

            } else {

                this.initScorecardClient();

                if (scoringMethod.equalsIgnoreCase("ml")) {

                    final MLScorecard mlScorecard = scorecard.getMlScorecard();

                    final MLScorecardFields loanScorecardFields = mlScorecard.getScorecardFields();

                    final PredictionResponse response = this.fetchScorecard(loanScorecardFields, scoringModel);

                    if (response != null) {
                        mlScorecard.setPredictionResponse(BigDecimal.valueOf(response.getProbability()),
                            response.getLabel(), response.getRequestId());
                    }

                } else if (scoringMethod.equalsIgnoreCase("stat")) {

                    final StatScorecard statScorecard = scorecard.getStatScorecard();

                    final MLScorecardFields loanScorecardFields = statScorecard.getScorecardFields();

                    final PredictionResponse response = this.fetchScorecard(loanScorecardFields, scoringModel);

                    if (response != null) {
                        final String method = response.getMethod();
                        final String color = response.getColor();
                        final BigDecimal probability = BigDecimal.valueOf(response.getProbability());

                        BigDecimal wilikis = null;
                        BigDecimal pillaisTrace = null;
                        BigDecimal hotelling = null;
                        BigDecimal roys = null;

                        if (method.equalsIgnoreCase("manova")) {
                            wilikis = BigDecimal.valueOf(response.getWilkisLambda());
                            pillaisTrace = BigDecimal.valueOf(response.getPillaisTrace());
                            hotelling = BigDecimal.valueOf(response.getHotellingTawley());
                            roys = BigDecimal.valueOf(response.getRoysReatestRoots());
                        }
                        statScorecard.setPredictionResponse(method, color, probability, wilikis, pillaisTrace, hotelling, roys);
                    }

                }
            }

        } else {
            return null;

        }

        this.scorecardRepository.save(scorecard);

        return scorecard;
    }

    private PredictionResponse fetchScorecard(final MLScorecardFields fields, final String scoringModel) {
        try {

            final Map<String, Object> predictionData = new HashMap<>();

            predictionData.put("age", fields.getAge());
            predictionData.put("sex", fields.getSex());
            predictionData.put("job", fields.getJob());
            predictionData.put("housing", fields.getHousing());
            predictionData.put("credit_amount", fields.getCreditAmount());
            predictionData.put("duration", fields.getDuration());
            predictionData.put("purpose", fields.getPurpose());

            return this.scorecardApiClient.algorithmsPredict(scoringModel, "0.0.1", null, null,
                    predictionData);

        } catch (ApiException e) {
            LOG.debug("An Error Occurred: {}", e.getLocalizedMessage());
        }
        return null;
    }

    @Override
    public CommandProcessingResult deleteScoringFeature(Long entityId) {

        this.context.authenticatedUser();

        final CreditScorecardFeature featureForDelete = this.featureRepository.findById(entityId)
                .orElseThrow(() -> new FeatureNotFoundException(entityId));
        if (featureForDelete.isDeleted()) {
            throw new FeatureNotFoundException(entityId);
        }

        final Collection<LoanProduct> loanProducts = this.loanProductRepository.retrieveLoanProductsByScorecardFeatureId(entityId);

        if (!loanProducts.isEmpty()) {
            throw new FeatureCannotBeDeletedException("error.msg.scorecard.feature.cannot.be.deleted.it.is.already.used.in.loan",
                    "This Scoring Feature cannot be deleted, it is already used in loan");
        }

        featureForDelete.delete();

        this.featureRepository.save(featureForDelete);

        return new CommandProcessingResultBuilder().withEntityId(featureForDelete.getId()).build();
    }

    /*
     * Guaranteed to throw an exception no matter what the data integrity issue is.
     */
    private void handleDataIntegrityIssues(final JsonCommand command, final Throwable realCause, final Exception dve) {

        if (realCause.getMessage().contains("name")) {
            final String name = command.stringValueOfParameterNamed("name");
            throw new PlatformDataIntegrityException("error.msg.scorecard.feature.duplicate.name",
                    "Scorecard Feature with name `" + name + "` already exists", "name", name);
        }

        LOG.error("Error occured.", dve);
        throw new PlatformDataIntegrityException("error.msg.scorecard.feature.unknown.data.integrity.issue",
                "Unknown data integrity issue with resource: " + realCause.getMessage());
    }

}
