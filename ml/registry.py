#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright created_byship.
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
ML registry

Registry object that will keep information about available algorithms and corresponding endpoints.
"""

from ml.classifiers import Classifier
from typing import Dict
from api.models import Algorithm, Dataset


def has_empty_values(data: dict):

    for key, value in data.items():
        if value == None:
            raise ValueError(f'{key} cannot be null')

    return False


class MLRegistry:
    def __init__(self):
        self.classifiers: Dict[int, Classifier] = {}

    def add_algorithms(self,
                       attrs=[{
                           "classifier": None,
                           "description": None,
                           "status": None,
                           "version": None,
                           "dataset": None,
                           "region": None,
                           "created_by": None
                       }]):

        for attr in attrs:

            if not has_empty_values(attr):
                #get dataset
                dataset, _ = Dataset.objects.get_or_create(
                    name=attr['dataset'], region=attr['region'])

                # get algorithm
                algorithm, _ = Algorithm.objects.get_or_create(
                    classifier=attr['classifier'].__class__.__name__,
                    description=attr['description'],
                    version=attr['version'],
                    status=attr['status'],
                    dataset=dataset,
                    created_by=attr['created_by'])
                self.classifiers[algorithm.id] = attr['classifier']

        return self.classifiers
