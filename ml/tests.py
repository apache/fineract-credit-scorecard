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

from ml.classifiers import GradientBoostClassifier, MLP, RandomForestClassifier, SVC
from ml.registry import MLRegistry
from django.test import TestCase

import inspect

test_data = {
    "age": 22,
    "sex": "female",
    "job": 2,
    "housing": "own",
    "credit_amount": 5951,
    "duration": 48,
    "purpose": "radio/TV"
}

expected_output = 'bad'


class MLTests(TestCase):
    def test_rf_algorithm(self):
        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(test_data)
        # self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual(expected_output, response['label'])

    # def test_svc_algorithm(self):
    #     my_alg = SVC()
    #     response = my_alg.compute_prediction(test_data)
    #     self.assertEqual('OK', response['status'])
    #     self.assertTrue('label' in response)
    #     self.assertEqual(expected_output, response['label'])

    def test_mlp_algorithm(self):
        my_alg = MLP()
        response = my_alg.compute_prediction(test_data)
        # self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual(expected_output, response['label'])

    def test_gb_algorithm(self):
        my_alg = GradientBoostClassifier()
        response = my_alg.compute_prediction(test_data)
        # self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual(expected_output, response['label'])

    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.classifiers), 0)

        # Random Forest classifier
        rf_algo = {
            'classifier': RandomForestClassifier(),
            'description': "Random Forest with simple pre and post-processing",
            'status': "production",
            'version': "0.0.1",
            'dataset': 'German',
            'region': 'Germany',
            'created_by': "xurror"
        }

        # add to registry
        registry.add_algorithms([rf_algo])
        # there should be one endpoint available
        self.assertEqual(len(registry.classifiers), 1)
