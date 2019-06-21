#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 14:31:21 2019

@author: ettignon
"""

import random
from collections import namedtuple

import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
    
    def __str__(self):
        string = ""
        for n in self.memory :
            string += "state :" + str(n[0]) + "\n"
            string += "action :" + str(n[1]) + "\n"
            string += "next_state :" + str(n[2]) + "\n"
            string += "reward :" + str(n[3]) + "\n"
            string += "\n"
        return(string)

class Net(nn.Module):

    def __init__(self, xin, yin, zin, xout, yout):
        super(Net, self).__init__()

        self.size_in = xin*yin*zin
        self.size_out = xout*yout
        self.conv1 = nn.Conv3d(1,100,3,padding=1)
        self.bnc1 = nn.BatchNorm3d(100)

        """
        self.conv2 = nn.Conv3d(100,100,3,padding=1)
        self.bnc2 = nn.BatchNorm3d(100)
        self.conv3 = nn.Conv3d(100,100,3,padding=1)
        self.bnc3 = nn.BatchNorm3d(100)
        self.conv4 = nn.Conv3d(100,100,3,padding=1)
        self.bnc4 = nn.BatchNorm3d(100)
        self.conv5 = nn.Conv3d(100,100,3,padding=1)
        self.bnc5 = nn.BatchNorm3d(100)
        self.conv6 = nn.Conv3d(100,100,3,padding=1)
        self.bnc6 = nn.BatchNorm3d(100)
        """


        self.lin1 = nn.Linear(100*self.size_in, 100*self.size_in)
        self.bnl1 = nn.BatchNorm1d(100*self.size_in)
        self.lin2 = nn.Linear(100*self.size_in, 100*self.size_out)
        self.bnl2 = nn.BatchNorm1d(100*self.size_out)
        self.lin3 = nn.Linear(100*self.size_out, self.size_out)
        # self.bnl3 = nn.BatchNorm1d(self.size_out)


    def forward(self, x):
        x = x.unsqueeze(0).unsqueeze(0)
        x = F.relu(self.bnc1(self.conv1(x)))
        """
        x = F.relu(self.bnc2(self.conv2(x)))
        x = F.relu(self.bnc3(self.conv3(x)))
        x = F.relu(self.bnc4(self.conv4(x)))
        x = F.relu(self.bnc5(self.conv5(x)))
        x = F.relu(self.bnc6(self.conv6(x)))
        """
        x = x.view(-1,100*self.size_in)

        # x = x.view(-1,self.size_in)
        x = F.relu(self.bnl1(self.lin1(x)))
        x = F.relu(self.bnl2(self.lin2(x)))
        x = self.lin3(x)


        #print(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

class DeepQLearning:
    
    def __init__(self, xin, yin, zin, xout, yout, majrate = 1000, gamma=0.3, learning_rate = 0.002, device = "cpu"):
        super(DeepQLearning, self).__init__()
        #Creation des deux réseaux de neurones.
        self.policy_net = Net(xin, yin, zin, xout, yout)
        self.target_net = Net(xin, yin, zin, xout, yout)
        if device != "cpu" :
            self.policy_net.cuda(torch.device(device))
            self.target_net.cuda(torch.device(device))
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        #Création de l'optimiser
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr = learning_rate)
        #Initialisation de MaJrate et de step. MaJrate représente le nombre d'action réalisé par l'agent avant la MaJ de target_net
        self.MaJrate = majrate
        self.step = 0
        #Création de la mémoire
        self.memory = ReplayMemory(1000)
        self.batch_size = 250
        #Initialisation des variables du Q-Learning
        self.Gamma = gamma
        self.values = False
        self.action = False
        self.state = False
        self.initial = True
        self.device = device
        self.xout = xout
        self.yout = yout

        self.nb_batch = 1

    def nouvellePartie(self):
        """Fonction à appeler pour prévenir l'agent que la prochaine action à prendre sera la première d'une nouvelle partie.
        Si cette fonction n'est pas appelé, l'agent pourra croire que la dernière action de la partie précédente l'aura mené à l'état où il se trouve en début de partie."""
        self.values = False
        self.action = False
        self.state = False
        self.initial = True
        
    def _MaJreseau_Batch(self):
        self.policy_net.train()
        #Si la mémoire n'est pas pleine, on attend son remplissage avant de mettre à jour le réseau.
        if len(self.memory) < self.batch_size:
            return

        # pbar = tqdm(range(self.nb_batch))

        for b in range(self.nb_batch):
            #On extrait les données du batch
            transitions = self.memory.sample(self.batch_size)
            batch = Transition(*zip(*transitions))
            state_batch = torch.cat(batch.state)
            action_batch = torch.cat(batch.action)
            reward_batch = torch.cat(batch.reward)
            #Pour les états déarrivé, il faut distinguer les états terminaux des autres
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=self.device, dtype=torch.uint8)
            non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
            #On calcul les valeurs attendus
            state_action_values = self.policy_net(state_batch).gather(1, action_batch.view(-1,1))
            next_state_values = torch.zeros(self.batch_size, device=self.device)
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
            expected_state_action_values = (next_state_values * self.Gamma) + reward_batch
            #On en déduit la loss
            loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
            #On optimise
            self.optimizer.zero_grad()
            loss.backward()
            for param in self.policy_net.parameters():
                param.grad.data.clamp_(-1, 1)
            self.optimizer.step()

            # pbar.set_postfix(batchloss_train=loss.item())
        
    def faireUnChoix(self,etat,liste_action_possible,tauxHasard=0.0,action_legal_seulement=False):
        """Fonction servant à faire prendre une decision à l'IA.
        Ses paramètres sont l'état actuel du jeu, ainsi que le pourcentage de chance de prendre une decision aléatoire (entre 0 et 1)."""
                
        #On restructure l'état.
        state = torch.tensor(etat,dtype=torch.float,device = self.device)
        
        #Si nous ne somme pas dans l'état initial, il faut mettre à jours le réseau.
        if(not self.initial):
            #self._MaJreseau(0.0,etat)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long, device = self.device), state, torch.tensor([0.0],dtype=torch.float, device = self.device))


            for i in range(self.nb_batch):
                self._MaJreseau_Batch()
        else:
            self.initial = False
        
        #On enrengistre l'état pour plus tard
        self.state = state

        #On calcule la valeur de chaque action possible
        self.policy_net.eval()
        self.values = self.policy_net(state)

        #Au hasard :
        # - Soit l'action est aléatoire
        # - Soit la meilleur action est choisi
        #Si le paramètre action_legale_seuement est à true, seul une action légal sera prise.
        if (random.random()>tauxHasard):
            if(not action_legal_seulement):
                self.action = self.values.argmax().item()
            else:
                lst_valeur = [-100.0] * (self.xout * self.yout)
                for action_possible in liste_action_possible:
                    act = action_possible[1]*self.xout+action_possible[0]
                    lst_valeur[act]=self.values[0][act]
                self.action = lst_valeur.index(max(lst_valeur))
            action = (self.action%self.xout, self.action//self.xout)
        else:
            action = random.choice(liste_action_possible)
            self.action = action[1]*self.xout+action[0]

        #Si le moment est venu, on met à jours le réseau secondaire
        self.step += 1
        if self.step > self.MaJrate:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self.step = 0
            
        return action
    
    def gagner(self):
        if(not self.initial):
            state = None
            #self._MaJreseau(1.0,etat,True)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long, device = self.device), state, torch.tensor([1.0],dtype=torch.float, device = self.device))
            self._MaJreseau_Batch()
        self.AncienEtat = ()
        self.AncienneValeur = ()
            
    def perdre(self):
        if(not self.initial):
            #On restructure l'état.
            state = None
            #self._MaJreseau(-1.0,etat,True)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long, device = self.device), state, torch.tensor([-1.0],dtype=torch.float, device = self.device))
            self._MaJreseau_Batch()
        self.AncienEtat = ()
        self.AncienneValeur = ()
            
    def egaliser(self):
        if(not self.initial):
            #On restructure l'état.
            state = None
            #self._MaJreseau(0.0,etat,True)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long, device = self.device), state, torch.tensor([0.0],dtype=torch.float, device = self.device))
            self._MaJreseau_Batch()
        self.AncienEtat = ()
        self.AncienneValeur = ()
        
        
