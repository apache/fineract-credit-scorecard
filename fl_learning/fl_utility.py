# fl_utility
import logging

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


log = logging.getLogger(__name__)

def preprocessing(dataset, data, test_size):
    """
    Preprocess dataset
    Parameters
    ----------
    data: DataFrame
        Pandas dataframe containing German dataset.
    """

    global processed_data
    global categorical
    global label_encoders

    # Reset global variables

    processed_data = None
    categorical = None
    label_encoders = {}

    if dataset == "German":
        # Drop savings account and checkings account columns as they contain a lot
        # of NaN values and may not always be available in real life scenarios
        data = data.drop(columns=['Saving accounts', 'Checking account'])

    dat_dict = data.to_dict()
    new_dat_dict = {}

    # rename columns(Make them lowercase and snakecase)
    for key, value in dat_dict.items():
        newKey = key
        if type(key) == str:
            newKey = newKey.lower().replace(' ', '_')
        # if newKey != key:
        new_dat_dict[newKey] = dat_dict[key]
    del dat_dict

    data = pd.DataFrame.from_dict(new_dat_dict)
    del new_dat_dict

    # print(data.describe())
    # print(data.describe(include='O'))

    cols = data.columns
    num_cols = data._get_numeric_data().columns
    categorical = list(set(cols) - set(num_cols))

    # Drop null rows
    data = data.dropna()

    # Encode text columns to number values
    for category in categorical:
        le = LabelEncoder()
        data[category] = le.fit_transform(data[category])
        label_encoders[category] = le

    for col in data.columns:
        if (col not in categorical):
            data[col] = (data[col].astype('float') - np.mean(data[col].astype('float'))) / np.std(
                data[col].astype('float'))

    # print(data.describe())
    # print(data.describe(include='O'))

    processed_data = data

    # Get Training parameters
    if dataset == "German":
        target_col = data.columns[-1]
        x = data.drop(columns=target_col, axis=1)
        y = data[target_col].astype('int')
    elif dataset == "Australian":
        x = data.drop(14, axis=1)
        y = data[14].astype('int')
    elif dataset == "Japanese":
        x = data.drop(15, axis=1)
        y = data[15].astype('int')
    elif dataset == "Taiwan":
        x = data.drop('default_payment_next_month', axis=1)
        y = data['default_payment_next_month'].astype('int')
    elif dataset == "Polish":
        x = data.drop('class', axis=1)
        y = data['class'].astype('int')
    elif dataset == 'Predict':
        data = pd.DataFrame(data)
        data.to_numpy()
        return data

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)

    return x_train.to_numpy(), x_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()





