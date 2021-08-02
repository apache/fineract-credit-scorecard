#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import json
import logging
from statistical_scripts.statistical_scoring import stat_score
from typing import Any, Dict

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, bad_request
from rest_framework.fields import CharField, FloatField, IntegerField
from rest_framework.response import Response

# from rest_framework import permissions
# from rest_framework_api_key.permissions import HasAPIKey

from api.models import Algorithm, Dataset, PredictionRequest
from api.serializers import AlgorithmSerializer, PredictionRequestSerializer, DatasetSerializer

from ml.classifiers import RandomForestClassifier

from server.wsgi import registry

# Create your views here.

log = logging.getLogger(__name__)


class AlgorithmViewSet(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = AlgorithmSerializer
    queryset = Algorithm.objects.all()

    @extend_schema(
        description='Predict credit risk for a loan',
        parameters=[
            OpenApiParameter(name='classifier',
                             description='The algorithm/classifier to use',
                             required=True,
                             examples=[OpenApiExample('Example 1',
                                                      value=RandomForestClassifier().__class__.__name__)]),
            OpenApiParameter(name='dataset',
                             description='The name of the dataset',
                             examples=[OpenApiExample('Example 1', value='german')]),
            OpenApiParameter(name='status',
                             description='The status of the algorithm',
                             deprecated=True,
                             examples=[OpenApiExample('Example 1', value='production')]),
            OpenApiParameter(name='version',
                             description='Algorithm version',
                             required=True,
                             examples=[OpenApiExample('Example 1', value='0.0.1')]),
        ],
        operation_id='algorithms_predict',
        request=Dict[str, Any],
        responses=inline_serializer(name="PredictionResponse",
                                    fields={"probability": FloatField(),
                                            "label": CharField(),
                                            "request_id": IntegerField()})
    )
    @action(detail=False, methods=['post'])
    def predict(self, request, format=None):

        try:
            classifier = self.request.query_params.get("classifier")
            region = self.request.query_params.get("dataset", "Germany")
            version = self.request.query_params.get("version")
            status = self.request.query_params.get("status", "production")

            if version is None:
                raise bad_request(request=request,
                                  data={"error": "Missing required query parameter: version"})
            if classifier is None:
                raise bad_request(request=request,
                                  data={"error": "Missing required query parameter: classifier"})

            algorithm: Algorithm = Algorithm.objects.filter(classifier=classifier,
                                                            status=status,
                                                            version=version,
                                                            dataset__name=region)[0]

            if algorithm is None:
                raise bad_request(request=request,
                                  data={"error": "ML algorithm is not available"})

            if classifier in ['manova', 'linearRegression', 'polynomialRegression']:
                prediction = stat_score(request.data, classifier)

            else:
                classifier = registry.classifiers[algorithm.id]
                prediction = classifier.compute_prediction(request.data)

            if "label" in prediction:
                label = prediction["label"]
            else:
                label = prediction['method']

            prediction_request = PredictionRequest(input=json.dumps(request.data),
                                                   response=prediction,
                                                   prediction=label,
                                                   feedback="",
                                                   algorithm=algorithm)
            prediction_request.save()

            prediction["request_id"] = prediction_request.id

            return Response(prediction)
        except Exception as e:
            raise APIException(str(e))


class PredictionRequestViewSet(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = PredictionRequestSerializer
    queryset = PredictionRequest.objects.all()


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = []
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()
