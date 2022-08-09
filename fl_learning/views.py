from django.shortcuts import render

# Create your views here.
import pickle
import sys
from collections import OrderedDict

import pandas as pd
import torch as t
import flwr as fl
from socket import socket, AF_INET, SOCK_STREAM
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from fl_learning.fl_utility import preprocessing
from fl_learning.fl_model import classifier_train, Net, accuracy, ClassifierClient
from ml.classifiers import RandomForestClassifier, MLP


class FLModelTrainAPIView(APIView):

    def post(self, request):
        # ------------------ read data ---------------------
        addr = request.data['addr']
        print(addr)
        try:
            data = pd.read_csv(addr, usecols=['Age', 'Sex', 'Job', 'Housing', 'Saving accounts', 'Checking account',
                                              'Credit amount', 'Duration', 'Purpose', 'Risk'])
        except Exception as e:
            raise APIException(str(e))
        print(data.head())

        # ------------------ connect to server ---------------------
        IP = '127.0.0.1'
        SERVER_PORT = 51000
        BUFLEN = 1024

        dataSocket = socket(AF_INET, SOCK_STREAM)
        try:
            dataSocket.connect((IP, SERVER_PORT))
        except:
            raise APIException("Unsuccessfully connect to the server, check the address and port")

        # ------------------ Train ---------------------------------
        command = "Train"
        dataSocket.send(command.encode())

        test_size = 0.01
        X_train, X_test, y_train, y_test = preprocessing("German", data, test_size)
        X_train_tensor = t.FloatTensor(X_train)
        y_train_tensor = t.tensor(y_train, dtype=t.long)
        X_test_tensor = t.FloatTensor(X_test)
        y_test_tensor = t.tensor(y_test, dtype=t.long)

        print(X_train[0])

        # Define the input and output
        input_channels = X_train_tensor.shape[1]
        output_channels = 2

        print(input_channels)

        # Initialize the model
        net = Net(input_channels, output_channels)
        # Define loss criterion
        criterion = t.nn.CrossEntropyLoss()
        # Define the optimizer
        optimizer = t.optim.Adam(net.parameters(), lr=0.001)
        # Number of epochs
        epochs = 5000

        client = ClassifierClient(net, X_train_tensor, y_train_tensor, criterion, optimizer, epochs)

        print(">>> Connect Flower server")
        fl.client.start_numpy_client("[::]:8085", client=client)

        # for name, param in net.named_parameters():
        #     if param.requires_grad:
        #         print(name, param.data)

        print(">>> Send Model to Server")
        serialized_model = pickle.dumps(net.state_dict())
        dataSocket.send(serialized_model)

        print(">>> Training Finish")

        return Response("Training Successfully")


class FLModelPredictAPIView(APIView):
    def post(self, request):
        # Data Input Format:
        age = request.data['age']
        sex = request.data['sex']
        job = request.data['job']
        housing = request.data['housing']
        credit = request.data['credit']
        duration = request.data['duration']
        purpose = request.data['purpose']

        data = {
            "age": int(age),
            "sex": sex,
            "job": int(job),
            "housing": housing,
            "credit_amount": int(credit),
            "duration": int(duration),
            "purpose": purpose
        }

        # test_data = {
        #     "age": 22,
        #     "sex": "female",
        #     "job": 2,
        #     "housing": "own",
        #     "credit_amount": 5951,
        #     "duration": 48,
        #     "purpose": "radio/TV"
        # }

        my_alg = MLP()  # only use for processing the data
        data = my_alg.preprocessing(data).to_numpy()
        print(data)
        data_tensor = t.FloatTensor(data)

        IP = '127.0.0.1'
        SERVER_PORT = 51000
        BUFLEN = 1024

        dataSocket = socket(AF_INET, SOCK_STREAM)
        try:
            dataSocket.connect((IP, SERVER_PORT))
        except:
            raise APIException("Unsuccessfully connect to the server, check the address and port")

        command = "Predict"
        dataSocket.send(command.encode())

        new_model_dict_string = dataSocket.recv(BUFLEN * 100)
        new_model_dict = pickle.loads(new_model_dict_string)
        net = Net(7, 2)
        net.load_state_dict(new_model_dict)
        with t.no_grad():
            net.eval()
            y_pred_vector = net(data_tensor)
            # val_loss = criterion(y_pred_vector, y_test_tensor)
            y_pred = net.predict(data_tensor)
            # acc = (y_test_tensor == y_pred).sum() / y_test_tensor.size(0)
        print("Prediction vector:", y_pred_vector)
        print("Prediction Result:", y_pred)
        return Response("Successfully")
