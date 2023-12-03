import numpy as np
import matplotlib.pyplot as plt
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
import time
from datetime import datetime
import json as js
import pandas as pd
from sklearn.preprocessing import StandardScaler
import argparse
import json

INPUT_SIZE = 30
HIDDEN_SIZE1 = 20
HIDDEN_SIZE2 = 20
OUTPUT_SIZE = 2
net_dims = [INPUT_SIZE, HIDDEN_SIZE1, HIDDEN_SIZE2, OUTPUT_SIZE]

# hyperperparameter
c = 0.05  # robustness parameter for LMT
lr = 0.1  # learning rate
rho = 0.25  # ADMM penalty parameter
mu = 0.00001  # Lip penalty parameter
lmbd = 0.0005  # L2 penalty parameter
ind_Lip = 1  # 1 Lipschitz regularization, 2 Enforcing Lipschitz bounds


class MeinNetz(nn.Module):
    def __init__(self):
        super(MeinNetz, self).__init__()
        self.lin1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE1)
        self.lin2 = nn.Linear(HIDDEN_SIZE1, HIDDEN_SIZE2)
        self.lin3 = nn.Linear(HIDDEN_SIZE2, OUTPUT_SIZE)

    def forward(self, x):
        x = torch.tanh(self.lin1(x))
        x = torch.tanh(self.lin2(x))
        x = self.lin3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num = 1
        for i in size:
            num *= i
        return num

    def extract_weights(self):
        weights = []
        biases = []
        for param_tensor in self.state_dict():
            tensor = self.state_dict()[param_tensor].detach().numpy().astype(np.float64)

            if 'weight' in param_tensor:
                weights.append(tensor)
            if 'bias' in param_tensor:
                biases.append(tensor)
        return weights, biases