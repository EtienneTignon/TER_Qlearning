#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 00:33:43 2019

@author: ettignon
"""

from Connect43D import Connect43D
from IA_deepqlearning import DeepQLearning
from IA_qlearning_v2 import QLearning
from tqdm import tqdm
from decimal import Decimal

def parties(joueur_1, joueur_2, nbr_partie_batch, c43d_haut=4, c43d_larg=4, c43d_long=4, c43d_lign=4, tauxHasard=1.0, montrerParties = False):
    victoirej1 = 0
    egalite = 0
    victoirej2 = 0
    pbar = tqdm(range(nbr_partie_batch))
    for i in pbar:   
        game = Connect43D(c43d_haut,c43d_larg,c43d_long,c43d_lign)
        if(montrerParties): print("Partie n" + str(i+1))
        if(i%2 == 0):
            game.actual_player=2
        joueur_1.nouvellePartie()
        joueur_2.nouvellePartie()
        jeuEnCours = True
        while(jeuEnCours):
            if(montrerParties): print(game.game)
            if(game.actual_player==1):
                action = joueur_1.faireUnChoix(game.game,game.get_move(),tauxHasard=tauxHasard,action_legal_seulement=True)
                game.do_move(action)
            else:
                action = joueur_2.faireUnChoix(game.game,game.get_move(),tauxHasard=tauxHasard,action_legal_seulement=True)
                game.do_move(action)
            if (game.is_finished()):
                    jeuEnCours = False
        if(montrerParties): print(game.game)
        if(game.winner==2):
            joueur_1.perdre()
            joueur_2.gagner()
            victoirej2 += 1
        elif(game.winner==1):
            joueur_1.gagner()
            joueur_2.perdre()
            victoirej1 += 1
        else:
            joueur_1.egaliser()
            joueur_2.egaliser()
            egalite += 1
    return (victoirej1,egalite,victoirej2)

def paquetsParties(joueur1, joueur2, nbr_batch=100, nbr_partie_batch=100, c43d_haut=4, c43d_larg=4, c43d_long=4, c43d_lign=4):
    batch = 1
    tauxHasard = 1.0
    txt = "Lr\tWin\tDraw\tLose\tElimination\n"
    while(batch <= nbr_batch):
        print("Paquet " + str(batch))
        #sleep(0.01)
        parties(joueur1, joueur2, nbr_partie_batch=nbr_partie_batch, c43d_haut=c43d_haut, c43d_larg=c43d_larg, c43d_long=c43d_long, c43d_lign=c43d_lign, tauxHasard=1.0)
        print("Debut des tests")
        resultat = parties(joueur1, joueur2, nbr_partie_batch=98, c43d_haut=c43d_haut, c43d_larg=c43d_larg, c43d_long=c43d_long, c43d_lign=c43d_lign, tauxHasard=0.0)
        r = parties(joueur1, joueur2, nbr_partie_batch=2, c43d_haut=c43d_haut, c43d_larg=c43d_larg, c43d_long=c43d_long, c43d_lign=c43d_lign, tauxHasard=0.0, montrerParties=True)
        resultat = (resultat[0]+r[0], resultat[1]+r[1], resultat[2]+r[2])
        txt += "{:.2E}".format(Decimal(tauxHasard)) + "\t" + str(resultat[0]) + "\t" + str(resultat[1]) + "\t" + str(resultat[2]) + "\n"
        print("{:.2E}".format(Decimal(tauxHasard)) + " " + str(resultat[0]) + " " + str(resultat[1]) + " " + str(resultat[2]))
        tauxHasard = tauxHasard/1.2
        batch += 1
        fichier = open("Resultat.txt", "w")
        fichier.write(txt)
  

c43d_long = 3
c43d_larg = 3
c43d_haut = 1
c43d_lign = 3    
#j1 = DeepQLearning(c43d_long,c43d_larg,c43d_haut,c43d_long,c43d_larg, gamma = 1, learning_rate = 0.001)
#j2 = DeepQLearning(c43d_long,c43d_larg,c43d_haut,c43d_long,c43d_larg, gamma = 1, learning_rate = 0.001)
j1=DeepQLearning(c43d_long,c43d_larg,c43d_haut,c43d_long,c43d_larg, gamma = 1, learning_rate = 0.001)
j2=QLearning()
paquetsParties(j1, j2, nbr_batch=1000, nbr_partie_batch=1000, c43d_haut=c43d_haut, c43d_larg=c43d_larg, c43d_long=c43d_long, c43d_lign=c43d_lign)