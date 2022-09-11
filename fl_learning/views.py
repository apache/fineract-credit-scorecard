from django.shortcuts import render

# Create your views here.
import pickle

import pandas as pd
import torch as t
import flwr as fl
from socket import socket, AF_INET, SOCK_STREAM

# Create your views here.
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from fl_learning.fl_utility import preprocessing
from fl_learning.fl_model import Net, ClassifierClient
from ml.classifiers import MLP


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

        input_channels = X_train_tensor.shape[1]
        output_channels = 2

        net = Net(input_channels, output_channels)
        criterion = t.nn.CrossEntropyLoss()
        optimizer = t.optim.Adam(net.parameters(), lr=0.001)
        epochs = 5000

        client = ClassifierClient(net, X_train_tensor, y_train_tensor, criterion, optimizer, epochs)

        print(">>> Connect Flower server")
        fl.client.start_numpy_client("[::]:8085", client=client)

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
            y_pred = net.predict(data_tensor)
        print("Prediction vector:", y_pred_vector)
        print("Prediction Result:", y_pred)
        return Response("Successfully")
