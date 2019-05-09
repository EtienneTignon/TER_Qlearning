#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:49:20 2019

@author: ettignon
"""


from Connect43D import Connect43D 
from IA_qlearning_v2 import QLearning
from agent import Agent
from Morpion import Morpion

joueurQ = QLearning()
qvictoire = 0
mvictoire = 0

i = 0
gagne = 0.0
while i < 5000:
    #game = Connect43D(3,3,3,3)
    game = Connect43D(5,1,7,4)
    joueurM = Agent(2, game)
    while True:    
        if (game.is_finished()):
            break
        move = joueurQ.prendreUneDecision(game.game,game.get_move(),(1.0/(i+1)))
        game.do_move(move)
        joueurM.update_action(move)
        if (game.is_finished()):
            break
        move = joueurM.next_action(200)
        game.do_move(move)
        joueurM.update_action(move)
    if(game.winner == 1):
        joueurQ.gagne()
        gagne += 1.0
        print("Bravo QLearning")
        qvictoire += 1
    elif(game.winner == 2):
        joueurQ.perdu()
        print("Bravo MCTS")
        mvictoire += 1
    else:
        joueurQ.gagne()
        print("Egalité")
    print(str((qvictoire,mvictoire)) + "/" + str(i+1))
    i += 1
    
i = 0
qvictoire = 0
mvictoire = 0
while i < 1000:
    #game = Connect43D(3,3,3,3)
    game = Connect43D(5,1,7,4)
    joueurM = Agent(2, game)
    while True:    
        if (game.is_finished()):
            break
        move = joueurQ.prendreUneDecision(game.game,game.get_move(),0.0)
        game.do_move(move)
        joueurM.update_action(move)
        if (game.is_finished()):
            break
        move = joueurM.next_action(200)
        game.do_move(move)
        joueurM.update_action(move)
    if(game.winner == 1):
        joueurQ.gagne()
        gagne += 1.0
        print("Bravo QLearning")
        qvictoire += 1
    elif(game.winner == 2):
        joueurQ.perdu()
        print("Bravo MCTS")
        mvictoire += 1
    else:
        joueurQ.gagne()
        print("Egalité")
    print(game.game)
    print(str((qvictoire,mvictoire)) + "/" + str(i+1))
    i += 1