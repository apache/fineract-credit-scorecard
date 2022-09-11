from collections import OrderedDict

import torch as t
import flwr as fl
from sklearn.metrics import accuracy_score



class Net(t.nn.Module):
    def __init__(self, input_channels, output_channels):
        super(Net, self).__init__()
        # Our network:
        # Linear1->relu->Batchnorm->Linear2->relu->Batchnorm->Dropout->Linear3->output
        # Softmax is added in the predict function
        # This applies Linear transformation to input data.
        self.fc1 = t.nn.Linear(input_channels, int(1.5 * input_channels))
        self.fc2 = t.nn.Linear(int(1.5 * input_channels), int(1.5 * input_channels))
        self.fc3 = t.nn.Linear(int(1.5 * input_channels), output_channels)

        self.relu = t.nn.ReLU()
        self.dropout = t.nn.Dropout(p=0.1)
        self.batchnorm1 = t.nn.BatchNorm1d(int(1.5 * input_channels))
        self.batchnorm2 = t.nn.BatchNorm1d(int(1.5 * input_channels))
        self.sigmoid = t.nn.Sigmoid()

    # This must be implemented
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.batchnorm1(x)
        x = self.relu(self.fc2(x))
        x = self.batchnorm2(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

    def predict(self, x):
        output = self.forward(x)
        prediction = t.argmax(output, 1)
        return prediction


def classifier_train(epochs, model, optimizer, X, y, criterion):
    losses = []
    for i in range(epochs):
        y_pred = model.forward(X)
        loss = criterion(y_pred, y)
        losses.append(loss.item())

        if i % 500 == 0:
            print("Epoch:", i, " Loss:", loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return losses


def accuracy(model,criterion, X, y):
    output_labels = model.forward(X)
    return criterion(output_labels, y), accuracy_score(model.predict(X), y)

class ClassifierClient(fl.client.NumPyClient):
    def __init__(self,net,X_train_tensor,y_train_tensor,criterion,optimizer,epochs):
        self.net = net
        self.X_train_tensor = X_train_tensor
        self.y_train_tensor = y_train_tensor
        self.criterion = criterion
        self.optimizer = optimizer
        self.epochs = epochs

    def get_parameters(self):
        return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.net.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: t.tensor(v) for k, v in params_dict})
        self.net.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        classifier_train(self.epochs, self.net, self.optimizer, self.X_train_tensor, self.y_train_tensor, self.criterion)
        return self.get_parameters(), self.X_train_tensor.shape[0], {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, acc = accuracy(self.net, self.X_test_tensor, self.y_test_tensor)
        return float(loss), self.X_test_tensor.shape[0], {"accuracy": float(acc)}
