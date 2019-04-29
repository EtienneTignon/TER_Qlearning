#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 14:31:21 2019

@author: ettignon
"""

from Morpion import Morpion
from IA_qlearning_v3 import QLearning
from IA_random import RandomPlayer

Jr = RandomPlayer()
Jq = QLearning()
i = 0.0
gagne = 0.0
égalité = 0.0
while i < 100000.0:
    game = Morpion()
    while True:    
        if (game.estFini):
            break
        game.doMove(Jr.smartRandom(game.getMove()))
        if (game.estFini):
            break
        game.doMove(Jq.prendreUneDecision(game.getStatus(),game.getMove()))
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
while i < 10000000.0:
    game = Morpion()
    while True:    
        if (game.estFini):
            break
        game.doMove(Jr.smartRandom(game.getMove()))
        if (game.estFini):
            break
        game.doMove(Jq._decisionRationel(game.getStatus(),game.getMove()))
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
i = 0.0
gagne = 0.0
égalité = 0.0
while i < 100.0:
    game = Morpion()
    while True:    
        if (game.estFini):
            break
        game.doMove(Jr.smartRandom(game.getMove()))
        print(game.game)
        if (game.estFini):
            break
        game.doMove(Jq._decisionRationel(game.getStatus(),game.getMove()))
        print(game.game)
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
    print(game.game)
    print(gagne/i)
Jq.enrengistrerMatriceTransition("p4.txt")