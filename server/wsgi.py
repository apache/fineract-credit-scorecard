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
WSGI config for scorecardapp project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information, visit
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
import inspect

from django.core.wsgi import get_wsgi_application

from ml.registry import MLRegistry
from ml.classifiers import GradientBoostClassifier, MLP, RandomForestClassifier, SVC

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'server.settings')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

registry = MLRegistry()

if ('runserver' in sys.argv or 'test' in sys.argv):
    # create ML registry

    try:
        rf = RandomForestClassifier()
        svc = SVC()
        mlp = MLP()
        gb = GradientBoostClassifier()
        
        registry.add_algorithm([
            # Random Forest classifier
            {'endpoint_name': "credit_scoring",
            'endpoint_classifier': "random_forest",
            'algorithm_object': rf,
            'algorithm_name': "random_forest",
            'algorithm_status': "production",
            'algorithm_version': "0.0.1",
            'created_by': "xurror",
            'algorithm_description': "Random Forest with simple pre- and post-processing",
            'algorithm_code': inspect.getsource(RandomForestClassifier)},
            
            # SVC classifier
            {'endpoint_name': "credit_scoring",
            'endpoint_classifier': "svc",
            'algorithm_object': svc,
            'algorithm_name': "svc",
            'algorithm_status': "testing",
            'algorithm_version': "0.0.1",
            'created_by': "xurror",
            'algorithm_description': "SVC Classifier with simple pre- and post-processing",
            'algorithm_code': inspect.getsource(SVC)},
            
            # MLP classifier
            {'endpoint_name': "credit_scoring",
            'endpoint_classifier': "mlp",
            'algorithm_object': mlp,
            'algorithm_name': "mlp",
            'algorithm_status': "testing",
            'algorithm_version': "0.0.1",
            'created_by': "xurror",
            'algorithm_description': "MLP Classifier with simple pre- and post-processing",
            'algorithm_code': inspect.getsource(MLP)},
            
            # Gradient Boost classifier
            {'endpoint_name': "credit_scoring",
            'endpoint_classifier': "gradient_boost",
            'algorithm_object': gb,
            'algorithm_name': "gradient_boost",
            'algorithm_status': "testing",
            'algorithm_version': "0.0.1",
            'created_by': "xurror",
            'algorithm_description': "Gradient Boost CLassifier with simple pre- and post-processing",
            'algorithm_code': inspect.getsource(GradientBoostClassifier)}])
        
    except Exception as e:
        print("Exception while loading the algorithms to the registry,", str(e))
        exit()
