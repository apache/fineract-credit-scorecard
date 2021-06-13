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

from api.views import ABTestViewSet, AlgorithmViewSet, RequestViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"algorithms", AlgorithmViewSet, basename="mlalgorithms")
router.register(r"requests", RequestViewSet, basename="mlrequests")
router.register(r"abtests", ABTestViewSet, basename="abtests")


urlpatterns = [
    # API docs
    path('api-docs/', SpectacularAPIView.as_view(), name='api-docs'),
    # Optional UI:
    path('api-docs/swagger-ui', SpectacularSwaggerView.as_view(url_name='api-docs'), name='swagger-ui'),
    path('api-docs/redoc', SpectacularRedocView.as_view(url_name='api-docs'), name='redoc'),

    # API Views
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/', include(router.urls)),
    # url(r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"),
    # url(r"^api/v1/stop_ab_test/(?P<ab_test_id>.+)", StopABTestView.as_view(), name="stop_ab"),
]
 