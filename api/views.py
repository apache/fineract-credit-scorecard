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

from api.models import GermanDataModel
from api.serializers import GermanDataModelSerializer, GroupSerializer, UserSerializer
from django.contrib.auth.models import Group, User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404, render

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = []


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScorecardViewSet(viewsets.ViewSet):
    """
    List all german data, or create a new GermanDataModel.
    """
    def list(self, request):
        queryset = GermanDataModel.objects.all()
        serializer = GermanDataModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = GermanDataModel.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = GermanDataModelSerializer(user)
        return Response(serializer.data)
        
    # def get(self, request, format=None):
    #     snippets = GermanDataModel.objects.all()
    #     serializer = GermanDataModelSerializer(snippets, many=True)
    #     return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def predict(self, request, format=None):
        data = self.get_object()
        queryset = GermanDataModel.objects.all()
        serializer = GermanDataModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
