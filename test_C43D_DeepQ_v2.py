#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:34:35 2019

@author: ettignon
"""

from IA_deepqlearning import DeepQLearning
from IA_random import RandomPlayer
from Connect43D import Connect43D

from random import random
from decimal import Decimal
from time import sleep

import torch

c43d_long = 3
c43d_larg = 3
c43d_haut = 1
c43d_lign = 3

def paquetpartie(nbr_batch_max=100, nbr_partie_batch=100, gamma=0.5, learningRate=0.001):
    joueur_dq = DeepQLearning(c43d_long,c43d_larg,c43d_haut,c43d_long,c43d_larg, gamma = gamma, learning_rate = learningRate)
    joueur_rand = RandomPlayer()
    nbr_partie = 1
    nbr_batch = 1
    tauxHasard = 1.0
    txt = "[gamma = " + str(gamma) + ", lr = " + str(learningRate) + "]\nLr\tWin\tDraw\tLose\tElimination\n"
    while(nbr_batch <= nbr_batch_max):
        nbr_partie = 1
        print("Batch " + str(nbr_batch))
        while(nbr_partie <= nbr_partie_batch):   
            game = Connect43D(c43d_haut,c43d_larg,c43d_long,c43d_lign)
            if(random() < 0.5):
                game.actual_player=2
            joueur_dq.nouvellePartie()
            jeuEnCours = True
            disqualification = False
            while(jeuEnCours):
                #sleep(0.01)
                if(game.actual_player==1):
                    action = joueur_dq.faireUnChoix(game.game,game.get_move(),tauxHasard=tauxHasard,action_legal_seulement=True)
                    if(action not in game.get_move()):
                        jeuEnCours = False
                        disqualification = True
                        print("Disqualification")
                    else:
                        game.do_move(action)
                else:
                    game.do_move(joueur_rand.smartRandom(game.get_move()))
                if (game.is_finished()):
                        jeuEnCours = False
            if(disqualification or game.winner==2):
                joueur_dq.perdre()
            elif(game.winner==1):
                joueur_dq.gagner()
            else:
                joueur_dq.egaliser()
            nbr_partie += 1
        nbr_partie = 1
        victoire=0
        defaite=0
        egualite=0
        elimination=0
        print("Debut des tests")
        while(nbr_partie <= 100):
            game = Connect43D(c43d_haut,c43d_larg,c43d_long,c43d_lign)
            if(random() < 0.5):
                game.actual_player=2
            joueur_dq.nouvellePartie()
            jeuEnCours = True
            disqualification = False
            while(jeuEnCours):
                #print(game.game)
                if(game.actual_player==1):
                    action = joueur_dq.faireUnChoix(game.game,game.get_move(),tauxHasard=tauxHasard,action_legal_seulement=True)
                    if(action not in game.get_move()):
                        joueur_dq.perdre()
                        elimination += 1
                    else:
                        game.do_move(action)
                else:
                    game.do_move(joueur_rand.smartRandom(game.get_move()))
                if (game.is_finished()):
                        jeuEnCours = False
            if(game.winner==2):
                joueur_dq.perdre()
                defaite += 1
            elif(game.winner==1):
                joueur_dq.gagner()
                victoire += 1
            else:
                joueur_dq.egaliser()
                egualite += 1
            nbr_partie += 1
        txt += "{:.2E}".format(Decimal(tauxHasard)) + "\t" + str(victoire) + "\t" + str(egualite) + "\t" + str(defaite) + "\t" + str(elimination) + "\n"
        print("{:.2E}".format(Decimal(tauxHasard)) + " " + str(victoire) + " " + str(egualite) + " " + str(defaite) + " " + str(elimination))
        tauxHasard = tauxHasard/2.0
        nbr_batch += 1
        fichier = open("Batch_g"+str(gamma)+"_lr"+str(learningRate)+".txt", "w")
        fichier.write(txt)
        torch.save(joueur_dq.policy_net,"reso.pt")

paquetpartie(nbr_batch_max=1000, gamma = 1, learningRate=0.005)

"""
gamma = 0.0
while(gamma <= 1.0):
    learningRate = 0.0001
    while(learningRate < 1.0):
        paquetpartie(nbr_batch_max=100, gamma=gamma)
        learningRate *= 5
    gamma += 0.1
"""