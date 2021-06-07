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

# Create your models here.

GenderTypes = models.Choices('male', 'female')
RiskTypes = models.Choices('good', 'bad')

class GermanDataModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField(blank=False)
    sex = models.CharField(blank=True, choices=GenderTypes.choices, max_length=10)
    job = models.CharField(max_length=100)
    housing = models.CharField(max_length=50)
    credit_amount = models.FloatField(blank=False, max_length=50)
    duration = models.IntegerField(blank=False)
    purpose = models.CharField(blank=True, max_length=50)
    risk = models.CharField(blank=True, choices=RiskTypes.choices, max_length=10)
    
    class Meta:
        ordering = ['created']

class Endpoint(models.Model):
    '''
    The Endpoint object represents ML API endpoint.

    Attributes
    ----------
        name: The name of the endpoint, it will be used in API URL,
        created_by: The string with owner name,
        created_at: The date when endpoint was created.
    '''
    name = models.CharField(max_length=128)
    classifier = models.CharField(max_length=128)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['created_at']
        
class MLAlgorithm(models.Model):
    '''
    The MLAlgorithm represent the ML algorithm object.

    Attributes
    ----------
        name: The name of the algorithm.
        description: The short description of how the algorithm works.
        code: The code of the algorithm.
        version: The version of the algorithm similar to software versioning.
        created_by: The name of the owner.
        created_at: The date when MLAlgorithm was added.
        parent_endpoint: The reference to the Endpoint.
    '''
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=128)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']
        
class MLAlgorithmStatus(models.Model):
    '''
    The MLAlgorithmStatus represent status of the MLAlgorithm which can change during the time.

    Attributes
    ----------
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        created_by: The name of creator.
        created_at: The date of status creation.
        parent_mlalgorithm: The reference to corresponding MLAlgorithm.
        parent_endpoint: The reference to corresonding Endpoint.
    '''
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name = "status")
    
    class Meta:
        ordering = ['created_at']

class MLRequest(models.Model):
    '''
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes
    ----------
        input_data: The input data to ML algorithm in JSON format.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_by: The name of creator.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response.
    '''
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)
    
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
        parent_mlalgorithm_1: The reference to the first corresponding MLAlgorithm.
        parent_mlalgorithm_2: The reference to the second corresponding MLAlgorithm.
    '''
    title = models.CharField(max_length=10000)
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    summary = models.CharField(max_length=10000, blank=True, null=True)

    parent_mlalgorithm_1 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_1")
    parent_mlalgorithm_2 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name="parent_mlalgorithm_2")
    
    class Meta:
        ordering = ['created_at']
