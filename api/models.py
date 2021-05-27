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
#

from django.db import models

# Create your models here.
class GermanDataModel(models.Model):
    GenderTypes = models.Choices('male', 'female')
    RiskTypes = models.Choices('good', 'bad')

    age = models.IntegerField(blank=True)
    sex = models.CharField(blank=True, choices=GenderTypes.choices, max_length=10)
    job = models.CharField(max_length=100)
    housing = models.CharField(max_length=50)
    credit_amount = models.FloatField(blank=True, max_length=50)
    duration = models.IntegerField(blank=True)
    purpose = models.CharField(blank=True, max_length=50)
    risk = models.CharField(blank=True, choices=RiskTypes.choices, max_length=10)