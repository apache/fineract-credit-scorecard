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

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, ShuffleSplit
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, recall_score, precision_score

class Model(object):
    """
    Basic Scorecard Model

    Warning: This class should not be used directly. Use derived classes
    instead.
    """

    def __init__(self,
                 classifier=None,
                 test_size=2.0,
                 n_splits=1,
                 random_state=None,
                 params=None):
                 
        self.classifier = classifier
        self.params = params
        self.random_state = random_state
        self.test_size = test_size
        self.n_splits = n_splits

        self.model = GridSearchCV(estimator=classifier,
                                  param_grid=params,
                                  cv=ShuffleSplit(test_size=0.20,
                                  n_splits=n_splits,
                                  random_state=0))
    
    def __str__(self):
        return f"""
        Model Object
        ----------------------------------------------------------------

        Classifier: {self.classifier().__class__.__name__}
        Test Size: {self.test_size}
        Random State: {self.random_state}
        Number of Splits: {self.n_splits}
        Parameter Grid: {self.params}

        {self.model}
        """

    def train(self, x_train, y_train):
        """
        Train scorecard model
        
        Args:
            x_train:
                array of training parameters
            y_train:
                pandas dataframe with training labels
        """

        self.model = self.model.fit(x_train, y_train.values.ravel())

    def predict(self, data):
        """
        Predict scorecard model

        Args:
            data: array
                Data to perform prediction on.
        """

        return self.model.predict(data)

    def accuracy(self, x_test, y_test):
        """
        Compute scorecard model accuracy

        Args:
            x_test: array
                The test parameters.
            y_test: array
                The labels
        """

        y_pred = self.predict(x_test)
        return accuracy_score(y_test, y_pred, normalize=False)

    def metrics(self, x_test, y_test):
        """
        Comput scorecard model metrics
        
        Args:
            x_test: array
                The test parameters.
            y_test: array
                The labels
        """

        y_pred = self.predict(x_test)
        cm = confusion_matrix(y_pred, y_test)
        accuracy = accuracy_score(y_test, y_pred, normalize=True)
        f1 = f1_score(self.y_test, y_pred, average="macro")
        recall = recall_score(y_test, y_pred, average="macro")
        precision = precision_score(y_test, y_pred, average="macro")
        return {"accuracy" : accuracy,
                "f1_score" : f1,
                "recall_score" : recall,
                "precision_score": precision}


class RandomForest(Model):
    """
    Model to predict credit risk using Random Forest Classifier
    
    Parameters
    ----------
    classifier: object, default: RandomForestClassifier
        sklearn classifier class.

    test_size: float, default: 0.2
        fraction of the dataset to use as test set.

    n_splits: int, default: 1
        number of splits.

    random_state: int, default: 0
        random state.

    params: dict: default: {'n_estimators' : [20, 30, 40], 'random_state' : [0]}
        model optimisation parameters
    """

    def __init__(self,
                 test_size=2.0,
                 n_splits=1,
                 random_state=0,
                 params={'n_estimators' : [20, 30, 40], 'random_state' : [0]}):
        self.classifier = RandomForestClassifier
        super(RandomForest, self).__init__(self.classifier,
                                           test_size,
                                           n_splits,
                                           random_state,
                                           params)

    def preprocessing(self, data):
        """
        Preprocess [German](https://raw.githubusercontent.com/humbletechy/Assign/master/datasets_9109_12699_german_credit_data.csv) dataset

        Parameters
        ----------
        data: DataFrame
            Pandas dataframe containing German dataset.
        """

        # Drop savings account and checkings account columns as they contain a lot
        # of NaN values and may not always be available in real life scenarios
        data = data.drop(columns = ['Saving accounts', 'Checking account'])
    
        cols = data.columns
        num_cols = data._get_numeric_data().columns
        categorical = list(set(cols) - set(num_cols))

        le = LabelEncoder()
        data = data.dropna()
        # Encode text columns to number values
        for category in categorical:
            data[category] = le.fit_transform(data[category])

        for col in data.columns:
            if(col not in categorical):
                data[col] = (data[col].astype('float') - np.mean(data[col].astype('float')))/np.std(data[col].astype('float'))

        # Get Training parameters
        target_col = data.columns[-1]
        x = data.drop(columns=target_col, axis=1)
        y = data[target_col].astype('int')


        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = self.test_size)
        x_train = pd.DataFrame(x_train)
        y_train = pd.DataFrame(y_train)

        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

        return (x_train, x_test, y_train, y_test)
