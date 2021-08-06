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

import logging
import os
import sys
import joblib

from django.core.wsgi import get_wsgi_application

from ml.registry import MLRegistry
from ml.classifiers import GradientBoostClassifier, MLP, RandomForestClassifier, SVC

log = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

registry = MLRegistry()

if ('runserver' in sys.argv or 'test' in sys.argv):
    
    # create ML registry
    try:
        zone = "german"
        
        registry.add_algorithms([
            # Random Forest classifier
            {'classifier': RandomForestClassifier(model=joblib.load(f'zoo/models/{zone}/rf_classifier.joblib'),
                                                  categorical=joblib.load(f'zoo/models/{zone}/categorical.joblib'),
                                                  label_encoders=joblib.load(f'zoo/models/{zone}/label_encoders.joblib')),
             'description': "Random Forest with simple pre and post-processing",
             'status': "production",
             'version': "0.0.1",
             'dataset': 'german',
             'region': 'Germany',
             'created_by': "xurror"},
            
            # SVC classifier
            {'classifier': SVC(model=joblib.load(f'zoo/models/{zone}/svc_classifier.joblib'),
                               categorical=joblib.load(f'zoo/models/{zone}/categorical.joblib'),
                               label_encoders=joblib.load(f'zoo/models/{zone}/label_encoders.joblib')),
             'description': "SVC Classifier with simple pre- and post-processing",
             'status': "testing",
             'version': "0.0.1",
             'dataset': 'german',
             'region': 'Germany',
             'created_by': "xurror"},
            
            # MLP classifier
            {'classifier': MLP(model=joblib.load(f'zoo/models/{zone}/mlp_classifier.joblib'),
                               categorical=joblib.load(f'zoo/models/{zone}/categorical.joblib'),
                               label_encoders=joblib.load(f'zoo/models/{zone}/label_encoders.joblib')),
             'description': "MLP Classifier with simple pre- and post-processing",
             'status': "testing",
             'version': "0.0.1",
             'dataset': 'german',
             'region': 'Germany',
             'created_by': "xurror"},
            
            # Gradient Boost classifier
            {'classifier': GradientBoostClassifier(model=joblib.load(f'zoo/models/{zone}/gb_classifier.joblib'),
                                                   categorical=joblib.load(f'zoo/models/{zone}/categorical.joblib'),
                                                   label_encoders=joblib.load(f'zoo/models/{zone}/label_encoders.joblib')),
             'description': "Gradient Boost CLassifier with simple pre- and post-processing",
             'status': "testing",
             'version': "0.0.1",
             'dataset': 'german',
             'region': 'Germany',
             'created_by': "xurror"}])
        
    except Exception as e:
        log.debug(f"Exception while loading the algorithms to the registry; {str(e)}")
        exit()
