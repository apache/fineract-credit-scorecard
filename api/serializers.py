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
"""
Serializer module
"""

from api.models import ABTest, Endpoint, GenderTypes, GermanDataModel, MLAlgorithm, MLAlgorithmStatus, MLRequest, RiskTypes
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class GermanDataModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GermanDataModel
        fields = ['id', 'age', 'sex', 'job', 'housing',
                  'credit_amount', 'duration', 'purpose']

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ["id", "name", "classifier", "created_by", "created_at"]
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlalgorithm) -> str:
        return MLAlgorithmStatus.objects.filter(parent_mlalgorithm=mlalgorithm).latest('created_at').status

    class Meta:
        model = MLAlgorithm
        read_only_fields = ["id", "name", "description", "code", "version", "created_by",
                            "created_at", "parent_endpoint", "current_status"]

        fields = read_only_fields
        
class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        read_only_fields = ["id", "active"]

        fields = ["id", "active", "status", "created_by",
                  "created_at", "parent_mlalgorithm"]

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = ["id", "input_data", "full_response", "response",
                            "created_by", "created_at", "parent_mlalgorithm"]
        
        fields = ["id", "input_data", "full_response", "response",
                  "feedback", "created_at", "parent_mlalgorithm"]

class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        read_only_fields = ["id", "ended_at", "created_at", "summary"]

        fields = ["id", "title", "created_by", "created_at", "ended_at", "summary",
                  "parent_mlalgorithm_1", "parent_mlalgorithm_2"]
