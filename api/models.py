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
API Models module
"""

from django.db import models


class Algorithm(models.Model):
    '''
    The MLAlgorithm represent the ML algorithm object.

    Attributes
    ----------
        name: The name of the algorithm.
        description: The short description of how the algorithm works.
        code: The code of the algorithm.
        version: The version of the algorithm similar to software versioning.
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        created_by: The name of the owner.
        created_at: The date when MLAlgorithm was added.
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"""
                ML Algorithm
                Name: {self.name}
                Description: {self.description}
                Version: {self.version}
                Status: {self.status}
                Created By: {self.created_by}
                Created At: {self.created_at}
                """
                
    class Meta:
        ordering = ['created_at']

class Request(models.Model):
    '''
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes
    ----------
        input_data: The input data to ML algorithm in JSON format.
        full_response: The full response of the ML algorithm in JSON format.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_by: The name of creator.
        created_at: The date when request was created.
        algorithm: The reference to MLAlgorithm used to compute response.
    '''
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"""
                ML Request
                Input Data: {self.input_data}
                Response: {self.response}
                Feedback: {self.feedback}
                Algorithm: {self.algorithm}
                Created By: {self.created_by}
                Created At: {self.created_at}
                """
                
    class Meta:
        ordering = ['created_at']

class ABTest(models.Model):
    '''
    The ABTest will keep information about A/B tests.

    Attributes
    ----------
        title: The title of test.
        created_by: The name of creator.
        created_at: The date of test creation.
        ended_at: The date of test stop.
        summary: The description with test summary, created at test stop.
        algorithm_1: The reference to the first corresponding ML Algorithm.
        algorithm_2: The reference to the second corresponding ML Algorithm.
    '''
    title = models.CharField(max_length=10000)
    summary = models.CharField(max_length=10000, blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    algorithm_1 = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name="algorithm_1")
    algorithm_2 = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name="algorithm_2")
    
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        ordering = ['created_at']
