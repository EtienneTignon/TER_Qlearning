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

c43d_long = 3
c43d_larg = 3
c43d_haut = 1
c43d_lign = 3
nbr_batch_max = 100
nbr_partie_batch = 100
joueur_dq = DeepQLearning(c43d_long,c43d_larg,c43d_haut,c43d_long,c43d_larg)
joueur_rand = RandomPlayer()
nbr_partie = 1
nbr_batch = 1

victoire=0
defaite=0
egualite=0
elimination=0
while(nbr_batch <= nbr_batch_max):
    nbr_partie = 1
    print("Batch " + str(nbr_batch))
    victoire = 0
    while(nbr_partie <= nbr_partie_batch):
        game = Connect43D(c43d_haut,c43d_larg,c43d_long,c43d_lign)
        if(random() < 0.5):
            game.actual_player=2
        joueur_dq.nouvellePartie()
        jeuEnCours = True
        disqualification = False
        while(jeuEnCours):
            #print(game.game)
            if(game.actual_player==1):
                action = joueur_dq.faireUnChoix(game.game,game.get_move(),tauxHasard=(1/(nbr_batch)))
                if(action not in game.get_move()):
                    jeuEnCours = False
                    disqualification = True
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
            victoire += 1
        else:
            joueur_dq.egaliser()
        nbr_partie += 1
    print("Taux de victoire : " + str(victoire))
    nbr_batch += 1