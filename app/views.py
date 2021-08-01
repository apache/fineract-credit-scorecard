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
Definition of views.
"""

from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    print("settings.BASE_URL")
    print(request.get_host())
    print("settings.BASE_URL 222")
    host = request.get_host()
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'host': host,
            'year':datetime.now().year,
        }
    )
  
def docs(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/docs.html',
        {
            'id': 'body-green',
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
  