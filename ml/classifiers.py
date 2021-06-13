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
Credit Risk Models

The module contains model definitions of various tested models for credit
assessment
"""

import joblib
import numpy as np
import pandas as pd

# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import StandardScaler
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV, ShuffleSplit
# from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, recall_score, precision_score

class Classifier(object):
    """
    Basic Scorecard Model

    Warning: This class should not be used directly. Use derived classes
    instead.
    """
    
    def __init__(self, model=None, categorical=[], label_encoders={}):
                 
        self.model = model
        self.categorical = categorical
        self.label_encoders = label_encoders
    
    # def __str__(self):
    #     return f"""
    #     Model Object
    #     ----------------------------------------------------------------

    #     Classifier: {self.classifier().__class__.__name__}
    #     Test Size: {self.test_size}
    #     Random State: {self.random_state}
    #     Number of Splits: {self.n_splits}
    #     Parameter Grid: {self.params}

    #     {self.model}
    #     """

    def preprocessing(self, data):
        """
        Preprocess python dict object for prediction

        Parameters
        ----------
        data: dict
            dictionary of data to predict
        """

        data = pd.DataFrame(data, index=[0])

        # fill missing values
        # data.fillna(self.values_fill_missing)

        categorical = self.categorical[:-1]

        le = self.label_encoders
        data = data.dropna()

        # convert categoricals
        for category in categorical:
            data[category] = le[category].transform(data[category])

        return data

    def predict(self, data):
        """
        Predict scorecard model

        Args:
            data: array
                Data to perform prediction on.
        """

        return self.model.predict_proba(data)
    
    def postprocessing(self, prediction):
        label = "bad"
        if prediction[1] > 0.5:
            label = "good"
        return {"probability": prediction[1], "label": label, "status": "OK"}
    
    def compute_prediction(self, data):
        try:
            input_data = self.preprocessing(data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

class RandomForestClassifier(Classifier):
    
    def __init__(self,
                 model=joblib.load('zoo/rf_classifier.joblib'),
                 categorical=joblib.load('zoo/categorical.joblib'),
                 label_encoders=joblib.load('zoo/label_encoders.joblib')):
        super(RandomForestClassifier, self).__init__(model, categorical, label_encoders)

class SVC(Classifier):
    
    def __init__(self,
                 model=joblib.load('zoo/svc_classifier.joblib'),
                 categorical=joblib.load('zoo/categorical.joblib'),
                 label_encoders=joblib.load('zoo/label_encoders.joblib')):
        super(SVC, self).__init__(model, categorical, label_encoders)

class MLP(Classifier):
    
    def __init__(self,
                 model=joblib.load('zoo/mlp_classifier.joblib'),
                 categorical=joblib.load('zoo/categorical.joblib'),
                 label_encoders=joblib.load('zoo/label_encoders.joblib')):
        super(MLP, self).__init__(model, categorical, label_encoders)

class GradientBoostClassifier(Classifier):
    
    def __init__(self,
                 model=joblib.load('zoo/gb_classifier.joblib'),
                 categorical=joblib.load('zoo/categorical.joblib'),
                 label_encoders=joblib.load('zoo/label_encoders.joblib')):
        super(GradientBoostClassifier, self).__init__(model, categorical, label_encoders)
