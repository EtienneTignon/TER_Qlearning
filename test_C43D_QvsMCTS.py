#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:49:20 2019

@author: ettignon
"""


from Connect43D import Connect43D 
from IA_qlearning_v1 import QLearning
from IA_mcts import mcts

joueurQ = QLearning()
qvictoire = 0
mvictoire = 0

i = 0
gagne = 0.0
while i < 1000:
    game = Connect43D()
    while True:    
        if (game.is_finished()):
            break
        game.do_move(joueurQ.prendreUneDecision(game.game,game.get_move(),(1.0/(i+1))))
        if (game.is_finished()):
            break
        game.do_move(mcts(game, 20, game.actual_player))
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
    game = Connect43D()
    while True:    
        if (game.is_finished()):
            break
        game.do_move(joueurQ.prendreUneDecision(game.game,game.get_move(),0.0))
        print(game.game)
        if (game.is_finished()):
            break
        game.do_move(mcts(game, 50, game.actual_player))
        print(game.game)
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