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
from fl_learning.fl_model import classifier_train, Net, accuracy,ClassifierClient


class FLModelTrainAPIView(APIView):

    def post(self, request):
        addr = request.data['addr']
        print(addr)
        try:
            data = pd.read_csv(addr)
        except Exception as e:
            raise APIException(str(e))
        print(data.head())
        IP = '127.0.0.1'
        SERVER_PORT = 50000
        BUFLEN = 1024

        dataSocket = socket(AF_INET, SOCK_STREAM)
        try:
            dataSocket.connect((IP, SERVER_PORT))
        except:
            raise APIException("Unsuccessfully connect to the server, check the address and port")


        command = "Train"
        dataSocket.send(command.encode())
        # Preparing Data
        german = pd.read_csv(addr)
        test_size = 0.20
        # processed_data = None
        # categorical = None
        # label_encoders = {}

        X_train, X_test, y_train, y_test = preprocessing("German", german, test_size)
        X_train_tensor = t.FloatTensor(X_train)
        y_train_tensor = t.tensor(y_train, dtype=t.long)
        X_test_tensor = t.FloatTensor(X_test)
        y_test_tensor = t.tensor(y_test, dtype=t.long)

        # Define the input and output
        input_channels = X_train_tensor.shape[1]
        output_channels = 2

        # Initialize the model
        net = Net(input_channels, output_channels)
        # Define loss criterion
        criterion = t.nn.CrossEntropyLoss()
        # Define the optimizer
        optimizer = t.optim.Adam(net.parameters(), lr=0.001)
        # Number of epochs
        epochs = 5000

        print(">>> Connect Flower server")
        client = ClassifierClient(net,X_train_tensor,y_train_tensor,criterion,optimizer,epochs)
        fl.client.start_numpy_client("[::]:8085", client=client)

        print(">>> Send Model to Server")
        serialized_model = pickle.dumps(net.state_dict())
        dataSocket.send(serialized_model)

        print(">>> Training Finish")

        return Response("Training Successfully")


class FLModelPredictAPIView(APIView):
    def post(self, request):
        addr = request.data['addr']
        print(addr)
        return Response("Successfully")
