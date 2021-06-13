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
import random
import datetime
from rest_framework.fields import CharField, FloatField, IntegerField

from server.wsgi import registry

from api.models import ABTest, Algorithm, Algorithm, Request
from api.serializers import ABTestSerializer, AlgorithmSerializer, RequestSerializer

# from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models import F

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer

# Create your views here.

class AlgorithmViewSet(viewsets.ModelViewSet):
    serializer_class = AlgorithmSerializer
    queryset = Algorithm.objects.all()

    @extend_schema(
        description='Predict credit risk for a loan',        
        parameters=[
            OpenApiParameter(
                name='classifier',
                description='Name of algorithm classifier',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'Example 1',
                        summary='Random Forest Classifier',
                        value='random_forest'
                    ),
                ],
            ),
            OpenApiParameter(
                name='status',
                description='The status of the algorithm',
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        'Example 1',
                        summary='Algorithm in production',
                        value='production'
                    ),
                ],
            ),
            OpenApiParameter(name='version', description='Algorithm version', required=True, type=str),
        ],
        operation_id='algorithms_predict',
        request=inline_serializer(name='Input Model Data',
                                  fields={'age': CharField(required=True),
                                          'sex': CharField(required=True,
                                                           max_length=25),
                                          'job': CharField(max_length=100),
                                          'housing': CharField(max_length=100),
                                          'credit_amount': FloatField(required=True),
                                          'duration': IntegerField(required=True),
                                          'purpose': CharField(max_length=100)
                                      }),
        responses={200: inline_serializer(name='Scoring successful',
                                          fields={"probability": FloatField(),
                                                   "label": CharField(max_length=100),
                                                   "status": CharField(max_length=100)}),
                   400: inline_serializer(name='Scoring falied',
                                          fields={"status": CharField(max_length=100),
                                           "message": CharField(max_length=100)})},
    )
    @action(detail=False, methods=['post'])
    def predict(self, request, format=None):
        algorithm_version = self.request.query_params.get("version")
        algorithm_status = self.request.query_params.get("status", "production")
        
        algs = Algorithm.objects.filter(status = algorithm_status)

        if algorithm_version is not None:
            algs = algs.filter(version = algorithm_version)

        num_algs = len(algs)
        
        if num_algs == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST)
            
        if num_algs != 1 and algorithm_status != "ab_testing":
            return Response(
                {"status": "Error", "message": "ML algorithm selection is ambiguous. Please specify algorithm version."},
                status=status.HTTP_400_BAD_REQUEST)
            
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = random.randrange(num_algs)

        algorithm = algs[alg_index]
        algorithm_object = registry.algorithms[algorithm.id]
        prediction = algorithm_object.compute_prediction(request.data)

        label = prediction["label"] if "label" in prediction else "error"
        ml_request = Request(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            algorithm=algs[alg_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)

class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

class ABTestViewSet(viewsets.ModelViewSet):
    serializer_class = ABTestSerializer
    queryset = ABTest.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save()
                
                # update status for first algorithm
                alg_1 = Algorithm.objects.get(pk=instance.algorithm_1.id)
                alg_1.status = "ab_testing"
                alg_1.save()
                
                # update status for second algorithm
                alg_2 = Algorithm.objects.get(pk=instance.algorithm_2.id)
                alg_2.status = "ab_testing"
                alg_2.save()

        except Exception as e:
            raise APIException(str(e))

    @action(detail=True, methods=['post'])
    def stop_ab_test(self, request, pk=None, format=None):

        try:
            ab_test = self.get_object()

            if ab_test.ended_at is not None:
                return Response({"message": "AB Test already finished."})

            date_now = datetime.datetime.now()
            # alg #1 accuracy
            all_responses_1 = Request.objects.filter(algorithm=ab_test.algorithm_1,
                                                     created_at__gt=ab_test.created_at,
                                                     created_at__lt=date_now).count()
            
            correct_responses_1 = Request.objects.filter(algorithm=ab_test.algorithm_1,
                                                         created_at__gt=ab_test.created_at,
                                                         created_at__lt=date_now, response=F('feedback')).count()
            
            accuracy_1 = correct_responses_1 / float(all_responses_1)
            print(all_responses_1, correct_responses_1, accuracy_1)

            # alg #2 accuracy
            all_responses_2 = Request.objects.filter(algorithm=ab_test.algorithm_2,
                                                     created_at__gt=ab_test.created_at,
                                                     created_at__lt=date_now).count()
            
            correct_responses_2 = Request.objects.filter(algorithm=ab_test.algorithm_2,
                                                         created_at__gt=ab_test.created_at,
                                                         created_at__lt=date_now,
                                                         response=F('feedback')).count()
            
            accuracy_2 = correct_responses_2 / float(all_responses_2)
            print(all_responses_2, correct_responses_2, accuracy_2)

            # select algorithm with higher accuracy
            alg_id_1, alg_id_2 = ab_test.algorithm_1, ab_test.algorithm_2
            # swap
            if accuracy_1 < accuracy_2:
                alg_id_1, alg_id_2 = alg_id_2, alg_id_1

            alg_1 = Algorithm.objects.get(pk=alg_id_1)
            alg_1.status = "production"
            alg_1.save()
            
            alg_2 = Algorithm.objects.get(pk=alg_id_2)
            alg_2.status = "testing"
            alg_2.save()
            
            summary = "Algorithm #1 accuracy: {}, Algorithm #2 accuracy: {}".format(accuracy_1, accuracy_2)
            ab_test.ended_at = date_now
            ab_test.summary = summary
            ab_test.save()

        except Exception as e:
            return Response({"status": "Error", "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "AB Test finished.", "summary": summary})
