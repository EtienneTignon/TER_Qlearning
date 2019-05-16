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
from collections import namedtuple

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

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(9, 100)
        self.fc2 = nn.Linear(100, 100)
        self.fc3 = nn.Linear(100, 100)
        self.fc4 = nn.Linear(100, 9)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

class DeepQAgent:
    
    def __init__(self, majrate = 100, gamma=0.1, learning_rate = 0.001, device = "cpu"):
        #Creation des deux réseaux de neurones.
        self.policy_net = Net()
        self.target_net = Net()
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        #Création de l'optimiser
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr = learning_rate)
        #Initialisation de MaJrate et de step. MaJrate représente le nombre d'action réalisé par l'agent avant la MaJ de target_net
        self.MaJrate = majrate
        self.step = 0
        #Création de la mémoire
        self.memory = ReplayMemory(10000)
        self.batch_size = 100
        #Initialisation des variables du Q-Learning
        self.Gamma = gamma
        self.values = False
        self.action = False
        self.state = False
        self.initial = True
        self.list_actions = [0,1,2,3,4,5,6,7,8]
        self.device = device

    def nouvellePartie(self):
        """Fonction à appeler pour prévenir l'agent que la prochaine action à prendre sera la première d'une nouvelle partie.
        Si cette fonction n'est pas appelé, l'agent pourra croire que la dernière action de la partie précédente l'aura mené à l'état où il se trouve en début de partie."""
        self.values = False
        self.action = False
        self.state = False
        self.initial = True
        self.list_actions = [0,1,2,3,4,5,6,7,8]
        
    def _MaJreseau_Batch(self):
        #Si la mémoire n'est pas pleine, on attend son remplissage avant de mettre à jour le réseau.
        if len(self.memory) < self.batch_size:
            return
        #On extrait les données du batch
        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        next_state_batch = torch.cat(batch.next_state)
        #On calcul les valeurs attendus
        state_action_values = self.policy_net(state_batch).gather(1, action_batch.view(-1,1))
        next_state_values = self.target_net(next_state_batch).max(1)[0].detach()
        expected_state_action_values = (next_state_values * self.Gamma) + reward_batch
        #On en déduit la loss
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
        #On optimise
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
    
    def _MaJreseau(self,recompense,etat,terminal = False):        
        next_State = etat.reshape(etat.size)
        next_State = [next_State]
        next_State = torch.tensor(next_State,dtype=torch.float)

        if(terminal):
            expected_state_action_values = [recompense]
        else:
            next_state_values = self.target_net(next_State)
            next_state_maxValues = next_state_values.max().item()
            expected_state_action_values = [self.Gamma*next_state_maxValues + recompense]
        
        expected_state_action_values = torch.tensor(expected_state_action_values, dtype=torch.float)
        state_action_values = self.values[0][self.action]
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values)

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()


    def faireUnChoix(self,etat,tauxHasard=0.0):
        """Fonction servant à faire prendre une decision à l'IA.
        Ses paramètres sont l'état actuel du jeu, ainsi que le pourcentage de chance de prendre une decision aléatoire (entre 0 et 1)."""
        
        #On restructure l'état.
        state = etat.reshape(etat.size)
        state = [state]
        state = torch.tensor(state,dtype=torch.float)
        
        #Si nous ne somme pas dans l'état initial, il faut mettre à jours le réseau.
        if(not self.initial):
            #self._MaJreseau(0.0,etat)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long), state, torch.tensor([0.0],dtype=torch.float))
            self._MaJreseau_Batch()
        else:
            self.initial = False
        
        #On enrengistre l'état pour plus tard
        self.state = state

        #On calcule la valeur de chaque action possible
        self.values = self.policy_net(state)

        #Au hasard :
        # - Soit l'action est aléatoire
        # - Soit la meilleur action est choisi
        if (random.random()>tauxHasard):
            self.action = self.values.argmax().item()
        else:
            self.action = random.choice(self.list_actions)
            
        #L'action est ensuite retiré des action que l'IA peute prendre au hasard plus tard.
        if(self.action in self.list_actions):
            self.list_actions.remove(self.action)
        
        #L'action est restructuré pour être comprise par l'environement
        action = (self.action//3, self.action%3)

        #Si le moment est venu, on met à jours le réseau secondaire
        self.step += 1
        if self.step > self.MaJrate:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self.step = 0
            
        return action
    
    def gagner(self,etat):
        if(not self.initial):
            #On restructure l'état.
            state = etat.reshape(etat.size)
            state = [state]
            state = torch.tensor(state,dtype=torch.float)
            #self._MaJreseau(1.0,etat,True)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long), state, torch.tensor([1.0],dtype=torch.float))
            self._MaJreseau_Batch()
        self.AncienEtat = ()
        self.AncienneValeur = ()
            
    def perdre(self,etat):
        if(not self.initial):
            #On restructure l'état.
            state = etat.reshape(etat.size)
            state = [state]
            state = torch.tensor(state,dtype=torch.float)
            #self._MaJreseau(-1.0,etat,True)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long), state, torch.tensor([-1.0],dtype=torch.float))
            self._MaJreseau_Batch()
        self.AncienEtat = ()
        self.AncienneValeur = ()
            
    def egaliser(self,etat):
        if(not self.initial):
            #On restructure l'état.
            state = etat.reshape(etat.size)
            state = [state]
            state = torch.tensor(state,dtype=torch.float)
            #self._MaJreseau(0.0,etat,True)
            self.memory.push(self.state, torch.tensor([self.action],dtype=torch.long), state, torch.tensor([0.0],dtype=torch.float))
            self._MaJreseau_Batch()
        self.AncienEtat = ()
        self.AncienneValeur = ()

dqa = DeepQAgent()
old = dqa.policy_net.state_dict()
jr = RandomPlayer()
i = 0
while(i<10000):
    victoire = 0
    defaite = 0
    egalite = 0
    coupIllegal = 0
    j = 0
    while(j<100):
        game = Connect43D(1,3,3,3)
        dqa.nouvellePartie()
        joueur = 1
        jeuEnCours = True
        disqualification = False
        while(jeuEnCours):
            if(joueur==1):
                action = dqa.faireUnChoix(game.game,1/(i+1))
                if(action not in game.get_move()):
                    jeuEnCours = False
                    disqualification = True
                    coupIllegal += 1
                else:
                    game.do_move(action)

                # print("résultat action")
                # print(game.game)

            else:
                move = jr.smartRandom(game.get_move())
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
    print(str(victoire)+" "+str(egalite)+" "+str(defaite-coupIllegal)+" "+str(coupIllegal), flush=True)
    i += 1
    
    
        