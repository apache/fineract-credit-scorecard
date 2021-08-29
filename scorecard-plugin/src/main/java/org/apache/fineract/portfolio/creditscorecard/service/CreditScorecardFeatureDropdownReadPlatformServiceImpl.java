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

import java.util.Arrays;
import java.util.List;
import org.apache.fineract.infrastructure.core.data.EnumOptionData;
import org.apache.fineract.portfolio.creditscorecard.domain.FeatureCategory;
import org.apache.fineract.portfolio.creditscorecard.domain.FeatureDataType;
import org.apache.fineract.portfolio.creditscorecard.domain.FeatureValueType;
import org.springframework.stereotype.Service;

@Service
public class CreditScorecardFeatureDropdownReadPlatformServiceImpl implements CreditScorecardFeatureDropdownReadPlatformService {

    @Override
    public List<EnumOptionData> retrieveValueTypes() {
        return Arrays.asList(CreditScorecardEnumerations.featureValueType(FeatureValueType.BINARY),
                CreditScorecardEnumerations.featureValueType(FeatureValueType.NOMINAL),
                CreditScorecardEnumerations.featureValueType(FeatureValueType.RATIO),
                CreditScorecardEnumerations.featureValueType(FeatureValueType.INTERVAL));
    }

    @Override
    public List<EnumOptionData> retrieveDataTypes() {
        return Arrays.asList(CreditScorecardEnumerations.featureDataType(FeatureDataType.STRING),
                CreditScorecardEnumerations.featureDataType(FeatureDataType.NUMERIC),
                CreditScorecardEnumerations.featureDataType(FeatureDataType.DATE));
    }

    @Override
    public List<EnumOptionData> retrieveCategoryTypes() {
        return Arrays.asList(CreditScorecardEnumerations.featureCategory(FeatureCategory.INDIVIDUAL),
                CreditScorecardEnumerations.featureCategory(FeatureCategory.ORGANISATION),
                CreditScorecardEnumerations.featureCategory(FeatureCategory.COUNTRY),
                CreditScorecardEnumerations.featureCategory(FeatureCategory.CREDIT_HISTORY),
                CreditScorecardEnumerations.featureCategory(FeatureCategory.LOAN));
    }
}
