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

from api.models import ABTest, Algorithm, Request
# from django.contrib.auth.models import User, Group
from rest_framework import serializers


class AlgorithmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Algorithm
        fields = ["id", "name", "description", "code", "version",
                  "status", "created_by", "created_at"]
  
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        read_only_fields = ["id", "input_data", "full_response", "response",
                            "algorithm", "created_by", "created_at"]
        
        fields = ["id", "input_data", "full_response", "response",
                  "feedback", "algorithm", "created_at"]

class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        read_only_fields = ["id", "summary", "ended_at", "created_at"]

        fields = ["id", "title", "summary", "ended_at", "algorithm_1",
                  "algorithm_2", "created_at", "created_by"]
