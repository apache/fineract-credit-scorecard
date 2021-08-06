#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

"""
API Models module
"""

from datetime import date
from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=128, unique=True)
    region = models.CharField(max_length=128, unique=True)


class Algorithm(models.Model):
    '''
    The MLAlgorithm represent the ML algorithm object.

    Attributes
    ----------
        classifier: The name of the algorithm.
        description: The short description of how the algorithm works.
        code: The code of the algorithm.
        version: The version of the algorithm similar to software versioning.
        status: The status of algorithm in the endpoint. Can be: testing, staging, production, ab_testing.
        created_by: The name of the owner.
        created_at: The date when MLAlgorithm was added.
    '''
    classifier: str = models.CharField(max_length=128)
    description: str = models.TextField(blank=True, null=True)
    version: str = models.CharField(max_length=128)
    status: str = models.CharField(max_length=128)
    dataset: Dataset = models.ForeignKey(Dataset,
                                         to_field="name",
                                         null=True,
                                         on_delete=models.SET_NULL)
    created_at: date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by: str = models.CharField(max_length=128)

    def __str__(self):
        return f"""
                ML Algorithm
                Classifier: {self.classifier}
                Description: {self.description}
                Version: {self.version}
                Status: {self.status}
                Created By: {self.created_by}
                Created At: {self.created_at}
                """

    class Meta:
        ordering = ['created_at']


class PredictionRequest(models.Model):
    '''
    The MLRequest will keep information about all requests to ML algorithms.

    Attributes
    ----------
        input: The input data to ML algorithm in JSON format.
        response: The full response of the ML algorithm in JSON format.
        prediction: The the prediction from ML request.
        feedback: The feedback about the response in JSON format.
        created_by: The name of creator.
        created_at: The date when request was created.
        algorithm: The reference to MLAlgorithm used to compute response.
    '''
    input = models.JSONField()
    response = models.JSONField()
    prediction = models.CharField(max_length=128)
    feedback = models.CharField(max_length=128, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    algorithm: Algorithm = models.ForeignKey(Algorithm,
                                             on_delete=models.DO_NOTHING,
                                             blank=True)
    created_at: date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=128)

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
