#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:34:35 2019

@author: ettignon
"""

import Connect43D as c43d
import random

game = c43d.Connect43D()
player = 0
i = 1

while(not game.is_finished()):
    i += 1
    coup_possible = game.get_move()
    print(coup_possible)
    coup_choisi = random.choice(coup_possible)
    print(coup_choisi)
    game.do_move(coup_choisi)
    print(game.game)