#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:44:45 2019

@author: ettignon
"""

from Connect43D import Connect43D
from IA_random import RandomPlayer

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

import random

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(9, 9)
        self.fc2 = nn.Linear(9, 9)
        self.fc3 = nn.Linear(9, 9)

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

class DeepQAgent:
    
    def __init__(self, majrate = 50, gamma=1e-1, learning_rate = 1e-1):
        #Creation des deux réseaux de neurones.
        self.policy_net = Net()
        self.target_net = Net()
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        #Création de l'optimiser
        self.optimizer = optim.RMSprop(self.policy_net.parameters())
        #Initialisation de MaJrate et de step. MaJrate représente le nombre d'action réalisé par l'agent avant la MaJ de target_net
        self.MaJrate = majrate
        self.step = 0
        #Initialisation des variables du Q-Learning
        self.Gamma = gamma
        self.LearningRate = learning_rate
        self.AncienEtat = ()
        self.AnciennesValeurs = ()
        
    def nouvellePartie(self):
        self.AncienEtat = ()
        self.AncienneValeur = ()
    
    def _MaJreseau(self,recompense,etat):
        newState = etat.reshape(etat.size)
        newState = [newState]
        newState = torch.tensor(newState,dtype=torch.float)
        expectedValues = self.target_net(newState)
        expectedValues = (self.Gamma*expectedValues)+((1-self.Gamma)*recompense)
        loss = F.smooth_l1_loss(self.AnciennesValeurs, expectedValues)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def faireUnChoix(self,etat,tauxHasard=0.0):
        if(not self.AncienEtat == ()):
            self._MaJreseau(0.0,etat)
        state = etat.reshape(etat.size)
        state = [state]
        state = torch.tensor(state,dtype=torch.float)
        values = self.target_net(state)
        if (random.random()>tauxHasard):
            action = values.argmax()
        else:
            action = random.randint(0,8)
        self.AncienEtat = etat
        self.AnciennesValeurs = values
        action = (action//3, action%3)
        self.step += 1
        if self.step > self.MaJrate:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self.step = 0
        return action
    
    def gagner(self,etat):
        if(not self.AncienEtat == ()):
            self._MaJreseau(100.0,etat)
        self.AncienEtat = ()
        self.AncienneValeur = ()
            
    def perdre(self,etat):
        if(not self.AncienEtat == ()):
            self._MaJreseau(-100.0,etat)
        self.AncienEtat = ()
        self.AncienneValeur = ()
            
    def egaliser(self,etat):
        if(not self.AncienEtat == ()):
            self._MaJreseau(0.0,etat)
        self.AncienEtat = ()
        self.AncienneValeur = ()

dqa = DeepQAgent()
old = dqa.policy_net.state_dict()
jr = RandomPlayer()
i = 0
while(i<100):
    victoire = 0
    defaite = 0
    egalite = 0
    coupIllegal = 0
    j = 0
    while(j<1000):
        game = Connect43D(1,3,3,3)
        joueur = 1
        jeuEnCours = True
        disqualification = False
        while(jeuEnCours):
            if(joueur==1):
                action = dqa.faireUnChoix(game.game,(1.0/(j+1)))
                if(action not in game.get_move()):
                    jeuEnCours = False
                    disqualification = True
                    coupIllegal += 1
                else:
                    game.do_move(action)
            else:
                game.do_move(jr.smartRandom(game.get_move()))
            if (game.is_finished()):
                jeuEnCours = False
            #print(game.game)
        if(disqualification or game.winner==2):
            dqa.perdre(game.game)
            defaite += 1
        elif(game.winner==1):
            dqa.gagner(game.game)
            victoire += 1
        else:
            dqa.egaliser(game.game)
            egalite += 1
        j += 1
        #print("Fin du jeu")
    print(str(victoire)+" . "+str(egalite)+" . "+str(defaite)+"(dont "+str(coupIllegal)+" coup interdit)")
    i += 1
    
    
        