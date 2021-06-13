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

from api.models import Algorithm

class MLRegistry:
    def __init__(self):
        self.algorithms = {}

    def add_algorithm(self, attrs=[{"algorithm_object": None, "algorithm_name": None,
                                    "algorithm_status": None, "algorithm_version": None, 
                                    "algorithm_description": None, "algorithm_code": None,
                                    "created_by": None}]):
        
        for attr in attrs:
            
            # get algorithm
            algorithm, _ = Algorithm.objects.get_or_create(name=attr['algorithm_name'],
                                                           description=attr['algorithm_description'],
                                                           code=attr['algorithm_code'],
                                                           version=attr['algorithm_version'],
                                                           status=attr['algorithm_status'],
                                                           created_by=attr['created_by'])
            # if created:
            #     status = MLAlgorithmStatus(status=attr['algorithm_status'],
            #                             created_by=attr['created_by'],
            #                             parent_mlalgorithm=ml_algorithm,
            #                             active=True)
            #     status.save()

            # add to registry
            self.algorithms[algorithm.id] = attr['algorithm_object']
