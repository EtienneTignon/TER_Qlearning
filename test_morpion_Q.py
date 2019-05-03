#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 14:31:21 2019

@author: ettignon
"""

from Morpion import Morpion
from IA_qlearning_v3 import QLearning
from IA_random import RandomPlayer
from math import sqrt

Jr = RandomPlayer()
Jq = QLearning()
"""
i = 0.0
gagne = 0.0
égalité = 0.0
while i < 100.0:
    game = Morpion()
    while True:    
        if (game.estFini):
            break
        game.doMove(Jr.smartRandom(game.getMove()))
        if (game.estFini):
            break
        game.doMove(Jq.prendreUneDecision(game.getStatus(),game.getMove(),0.5))
    if game.winner == 1:
        print("RandGagne")
        Jq.perdu(game.getStatus())
    elif game.winner == 2:
        print("Q gagne")
        Jq.gagne(game.getStatus())
        gagne += 1.0
    else:
        print("égalité")
        Jq.gagne(game.getStatus())
        égalité += 1.0
    i += 1.0
    print(gagne/i)
i = 0.0
gagne = 0.0
égalité = 0.0
while i < 100.0:
    game = Morpion()
    while True:    
        if (game.estFini):
            break
        game.doMove(Jr.smartRandom(game.getMove()))
        if (game.estFini):
            break
        game.doMove(Jq.prendreUneDecision(game.getStatus(),game.getMove(),0.0))
    if game.winner == 1:
        print("RandGagne")
        Jq.perdu(game.getStatus())
    elif game.winner == 2:
        print("Q gagne")
        Jq.gagne(game.getStatus())
        gagne += 1.0
    else:
        print("égalité")
        Jq.gagne(game.getStatus())
        égalité += 1.0
    i += 1.0
    print(gagne/i)
Jq.enrengistrerMatriceTransition("p4.txt")
"""
j = 1.0
while(True):
    i = 0.0
    gagne = 0.0
    egalite = 0.0
    perdu = 0.0
    while i < 10000.0:
        game = Morpion()
        while True:    
            if (game.estFini):
                break
            game.doMove(Jr.smartRandom(game.getMove()))
            if (game.estFini):
                break
            game.doMove(Jq.prendreUneDecision(game.getStatus(),game.getMove(),(1/(2*j))))
        if game.winner == 1:
            Jq.perdu()
            perdu += 1.0
        elif game.winner == 2:
            Jq.gagne()
            gagne += 1.0
        else:
            Jq.gagne()
            egalite += 1.0
        i += 1.0
    j += 1.0
    print("Victoire : " + str(gagne/100.0) + " / Egalité : " + str(egalite/100.0) + " / Perdu : " + str(perdu/100.0))
    Jq.enrengistrerMatriceTransition("test.txt")