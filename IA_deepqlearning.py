#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 14:31:21 2019

@author: ettignon
"""

import random

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

    def __init__(self, sizeEtat, sizeAction):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(sizeEtat, 3*sizeEtat)
        self.fc2 = nn.Linear(3*sizeEtat, 3*sizeAction)
        self.fc3 = nn.Linear(3*sizeAction, sizeAction)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

class DeepQLearning:
    
    def __init__(self, sizeEtat, sizeAction, learning_rate = 1e-4, majrate = 100, gamma=0.2):
        #Creation des deux réseaux de neurones.
        self.policy_net = Net(sizeEtat, sizeAction)
        self.target_net = Net(sizeEtat, sizeAction)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        #Création de l'optimiser
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr = learning_rate)
        
        