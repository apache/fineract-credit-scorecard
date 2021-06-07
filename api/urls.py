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

"""
Definition of urls for scorecardapp.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from rest_framework import routers
from app import forms, views
from api import views as apiViews


router = routers.DefaultRouter()
router.register(r'users', apiViews.UserViewSet)
router.register(r'groups', apiViews.GroupViewSet)
router.register(r'scorecard', apiViews.ScorecardViewSet, basename='scorecard')


urlpatterns = [
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),

    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

    # API Views
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
