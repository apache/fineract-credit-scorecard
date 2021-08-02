import json
import logging
import numpy as np
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from scipy.stats import norm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from statsmodels.multivariate.manova import MANOVA
import configparser
import csv


log = logging.getLogger(__name__)

def linear_regression(input_row, data, categorical):

    data = data.dropna()
    data.loc[len(data)] = input_row
    le = LabelEncoder()
    for val in categorical:
        data[val] = le.fit_transform(data[val])
    for col in data.columns:
        if(col not in categorical):
            data[col] = (data[col] - np.mean(data[col]))/np.std(data[col])

    split = 0.8
    split_idx = int(len(data)*split)
    data_train = data[:split_idx]
    data_test = data[split_idx:]

    y_train = data_train[10]
    x_train = data_train.loc[:, data_train.columns != 10]
    y_test = data_test[10]
    x_test = data_test.loc[:, data_test.columns != 10]

    reg = LinearRegression().fit(x_train, y_train)

    predictions = reg.predict(x_test)
    for i in range(len(predictions)):
        if predictions[i] > 0.5:
            predictions[i] = 1
        else:
            predictions[i] = 0

    count = 0
    y_test = np.array(y_test)
    for i in range(len(predictions)):
        if(y_test[i] == predictions[i]):
            count = count + 1
    accuracy = count/len(predictions)

    if(predictions[len(x_test)-1] < 0.5):
        color = "red"
    else:
        color = "green"

    return {"method": "LinReg", "color": color, "prediction": 100*accuracy}


def polynomial_regression(input_row, data, categorical):

    data = data.dropna()
    data.loc[len(data)] = input_row
    le = LabelEncoder()
    for val in categorical:
        data[val] = le.fit_transform(data[val])

    for col in data.columns:
        if(col not in categorical):
            data[col] = (data[col] - np.mean(data[col]))/np.std(data[col])

    split = 0.7
    split_idx = int(len(data)*split)
    data_train = data[:split_idx]
    data_test = data[split_idx:]

    y_train = data_train[10]
    x_train = data_train.loc[:, data_train.columns != 10]
    y_test = data_test[10]
    x_test = data_test.loc[:, data_test.columns != 10]

    model = Pipeline([('poly', PolynomialFeatures(degree=2)),
                     ('linear', LinearRegression(fit_intercept=False))])
    reg = model.fit(x_train, y_train)

    # reg = LinearRegression().fit(x_train, y_train)

    predictions = reg.predict(x_test)
    for i in range(len(predictions)):
        if predictions[i] > 0.5:
            predictions[i] = 1
        else:
            predictions[i] = 0

    count = 0
    y_test = np.array(y_test)
    for i in range(len(predictions)):
        if(y_test[i] == predictions[i]):
            count = count + 1
    accuracy = count/len(predictions)

    if(predictions[len(x_test)-1] < 0.5):
        color = "red"
    else:
        color = "green"

    return {"method": "PolyReg", "color": color, "prediction": 100*accuracy}


def manova(test_row, data, categorical):

    data = data.dropna()
    data.loc[len(data)] = test_row

    le = LabelEncoder()
    for val in categorical:
        data[val] = le.fit_transform(data[val])

    for col in data.columns:
        if(col not in categorical):
            data[col] = (data[col] - np.mean(data[col]))/np.std(data[col])

    test_row = data.iloc[len(data)-1]
    data.drop([len(data)-1])

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

    WL_good = out_good[0][0]
    PT_good = out_good[1][0]
    HT_good = out_good[2][0]
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

    WL_test_good = out_test[0][0]
    PT_test_good = out_test[1][0]
    HT_test_good = out_test[2][0]
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

    scorecard = {"method": "MANOVA", "WL_good": WL_good,
                 "WL_test_good": WL_test_good, "WL_bad": WL_bad, "WL_test_bad": WL_test_bad}

    ret = "WL good : " + str(WL_good) + " WL test good : " + str(WL_test_good) + \
        "\nWL bad : " + \
        str(WL_bad) + " WL test bad : " + \
        str(WL_test_bad)

    return scorecard


def stat_score(input_row, model_type):
    df = pd.read_csv(f'zoo/data/german.csv', index_col=0)
    data = df.drop(columns=['Saving accounts', 'Checking account'])
    cols = data.columns
    num_cols = data._get_numeric_data().columns
    categorical = list(set(cols) - set(num_cols))

    try:
        if(model_type == 'manova'):
            output = manova(input_row, data, categorical)
        elif(model_type == 'linearRegression'):
            output = linear_regression(input_row, data, categorical)
        elif(model_type == 'polynomialRegression'):
            output = polynomial_regression(input_row, data, categorical)

        return output

    except Exception as e:
        log.debug(f"An Exception Occurred; {str(e)}")
