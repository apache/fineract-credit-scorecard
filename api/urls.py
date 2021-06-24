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
Definition of urls for api resource.
"""

from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api.views import AlgorithmViewSet, DatasetViewSet, PredictionRequestViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"algorithms", AlgorithmViewSet, basename="algorithms")
router.register(r"datasets", DatasetViewSet, basename="datasets")
router.register(r"requests", PredictionRequestViewSet, basename="prediction_requests")

urlpatterns = [
    # API docs
    path('api-docs/', SpectacularAPIView.as_view(), name='api-docs'),
    # Optional UI:
    path('api-docs/swagger-ui', SpectacularSwaggerView.as_view(url_name='api-docs'), name='swagger-ui'),
    path('api-docs/redoc', SpectacularRedocView.as_view(url_name='api-docs'), name='redoc'),

    # API Views
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/', include(router.urls)),
]
 