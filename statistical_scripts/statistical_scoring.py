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

import logging
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from statsmodels.multivariate.manova import MANOVA
from rest_framework.exceptions import APIException

log = logging.getLogger(__name__)


def linear_regression(input_data, data):

    y = data['risk']
    x = data.drop(columns=['risk'])

    reg = LinearRegression().fit(x, y)

    predictions = reg.predict(input_data)

    probability = predictions[0]
    color = 'green' if probability > 0.5 else 'red'

    return {"color": color, "probability": probability}


def polynomial_regression(input_data, data):

    y = data['risk']
    x = data.drop(columns=['risk'])

    model = Pipeline([('poly', PolynomialFeatures(degree=2)),
                      ('linear', LinearRegression(fit_intercept=False))])
    reg = model.fit(x, y)

    predictions = reg.predict(input_data)

    probability = predictions[0]
    color = 'green' if probability > 0.5 else 'red'

    return {"color": color, "probability": probability}


def manova(test_row, data, categorical):

    data = data.dropna()
    data.loc[len(data)] = test_row

    le = LabelEncoder()
    for val in categorical:
        data[val] = le.fit_transform(data[val])

    for col in data.columns:
        if (col not in categorical):
            data[col] = (data[col] - np.mean(data[col])) / np.std(data[col])

    test_row = data.iloc[len(data) - 1]
    data.drop([len(data) - 1])

    data_good = data[data[10] == 0]
    data_bad = data[data[10] == 1]

    x_good = data_good.drop([10, 9], axis=1)
    y_good = data_good[[9]]
    x_bad = data_bad.drop([10, 9], axis=1)
    y_bad = data_bad[[9]]

    man_good = MANOVA(endog=x_good, exog=y_good)
    man_bad = MANOVA(endog=x_bad, exog=y_bad)

    output_good = man_good.mv_test()
    output_bad = man_bad.mv_test()

    out_good = np.array(output_good['x0']['stat'])
    out_bad = np.array(output_bad['x0']['stat'])

    # Wilki's Lambda
    WL_good = out_good[0][0]

    # Pillai's Trace
    PT_good = out_good[1][0]

    # Hotelling-Lawley Trace
    HT_good = out_good[2][0]

    # Roy's Greatest Roots
    RGR_good = out_good[3][0]

    WL_bad = out_bad[0][0]
    PT_bad = out_bad[1][0]
    HT_bad = out_bad[2][0]
    RGR_bad = out_bad[3][0]

    x = test_row.drop([10, 9])
    y = test_row[[9]]

    data_test_x = x_good.append(x)
    data_test_y = y_good.append(y)

    man_test = MANOVA(endog=data_test_x, exog=data_test_y)
    output_test = man_test.mv_test()

    out_test = np.array(output_test['x0']['stat'])

    # Wilki's Lambda
    WL_test_good = out_test[0][0]

    # Pillai's Trace
    PT_test_good = out_test[1][0]

    # Hotelling-Lawley Trace
    HT_test_good = out_test[2][0]

    # Roy's Greatest Roots
    RGR_test_good = out_test[3][0]

    data_test_x = x_bad.append(x)
    data_test_y = y_bad.append(y)

    man_test = MANOVA(endog=data_test_x, exog=data_test_y)
    output_test = man_test.mv_test()

    out_test = np.array(output_test['x0']['stat'])

    WL_test_bad = out_test[0][0]
    PT_test_bad = out_test[1][0]
    HT_test_bad = out_test[2][0]
    RGR_test_bad = out_test[3][0]

    scorecard = {
        "method": "MANOVA",
        "WL_good": WL_good,
        "WL_test_good": WL_test_good,
        "WL_bad": WL_bad,
        "WL_test_bad": WL_test_bad
    }

    ret = "WL good : " + str(WL_good) + " WL test good : " + str(WL_test_good) + \
        "\nWL bad : " + \
        str(WL_bad) + " WL test bad : " + \
        str(WL_test_bad)

    return scorecard


def rename_df_columns(df):
    dat_dict = df.to_dict()
    new_dat_dict = {}

    for key, value in dat_dict.items():
        newKey = key
        if type(key) == str:
            newKey = newKey.lower().replace(' ', '_')
        new_dat_dict[newKey] = dat_dict[key]
    del dat_dict

    df = pd.DataFrame.from_dict(new_dat_dict)
    del new_dat_dict

    return df


def prepare_data(data):

    data['job'] = data['job'].astype('int')

    cols = data.columns
    num_cols = data._get_numeric_data().columns
    categorical = list(set(cols) - set(num_cols))

    le = LabelEncoder()
    for val in categorical:
        data[val] = le.fit_transform(data[val])

    for col in data.columns:
        if col not in categorical:
            data[col] = (data[col] - np.mean(data[col])) / np.std(data[col])

    input_data = data.iloc[len(data) - 1]
    input_data = input_data.to_dict()
    input_data = pd.DataFrame(input_data, index=[0]).drop(columns=['risk'])

    return data, input_data


def stat_score(input_data, model_type):
    df = pd.read_csv(f'zoo/data/german.csv', index_col=0)
    dataset = df.drop(columns=['Saving accounts', 'Checking account'])
    dataset = dataset.dropna()

    # rename columns(Make them lowercase and snakecase)
    dataset = rename_df_columns(dataset)

    # Assume input risk is bad
    input_data['risk'] = 'bad'
    dataset.loc[len(dataset)] = input_data

    # Prepare and normalize data
    dataset, input_data = prepare_data(dataset)

    try:
        if model_type == 'manova':
            raise APIException(
                "Statistical Method Manova is not implemented yet")
            # output = manova(input_data, dataset)

        elif model_type == 'linearRegression':
            output = linear_regression(input_data, dataset)

        elif model_type == 'polynomialRegression':
            output = polynomial_regression(input_data, dataset)

        output['method'] = model_type
        return output

    except Exception as e:
        log.debug(f"An Exception Occurred; {str(e)}")
