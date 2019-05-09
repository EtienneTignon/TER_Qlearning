#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 13:26:44 2019

@author: ettignon
"""

import numpy as np

class Morpion:
    def __init__(self):
        self.game = np.full((3,3), 0, dtype=np.dtype('i8'))
        self.winner = 0
        self.actual_player = 1
        self.isFinished = False
        self.coupRestant = 9
    
    def _checkWin(self, coup):
        if coup[0]==0:
            if self.game[0][0]==self.game[0][1] and self.game[0][0]==self.game[0][2]:
                return True
        if coup[0]==1:
            if self.game[1][0]==self.game[1][1] and self.game[1][0]==self.game[1][2]:
                return True
        if coup[0]==2:
            if self.game[2][0]==self.game[2][1] and self.game[2][0]==self.game[2][2]:
                return True
        if coup[1]==0:
            if self.game[0][0]==self.game[1][0] and self.game[0][0]==self.game[2][0]:
                return True
        if coup[1]==1:
            if self.game[0][1]==self.game[1][1] and self.game[0][1]==self.game[2][1]:
                return True
        if coup[1]==2:
            if self.game[0][2]==self.game[1][2] and self.game[0][2]==self.game[2][2]:
                return True
        if coup[0]==coup[1]:
            if self.game[0][0]==self.game[1][1] and self.game[0][0]==self.game[2][2]:
                return True
        if coup[0]==(2-coup[1]):
            if self.game[0][2]==self.game[1][1] and self.game[0][2]==self.game[2][0]:
                return True
        return False
    
    def is_finished(self):
        return self.isFinished
    
    def do_move(self, coup):
        x = coup[0]
        y = coup[1]
        if self.game[x][y] == 0 and not self.isFinished:
            self.game[x][y] = self.actual_player
            self.coupRestant -= 1
            if self._checkWin(coup):
                self.isFinished=True
                self.winner=self.actual_player
            elif self.coupRestant==0:
                self.isFinished=True
            else:
                if self.actual_player == 1:
                    self.actual_player = 2
                else:
                    self.actual_player = 1
        else:
            print("Vous en pouvez pas jouer ce coup")
            
    def get_move(self):
        listeCoupPossible = []
        x = 0
        while x<3:
            y = 0
            while y < 3:
                if self.game[x][y]==0:
                    listeCoupPossible.append((x,y))
                y += 1
            x += 1
        return listeCoupPossible
    
    def getStatus(self):
        game = self.game.reshape(9)
        game = tuple(game)
        return (game,self.actual_player)