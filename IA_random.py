#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:30:16 2019

@author: ettignon
"""

from random import randrange
from random import choice

class RandomPlayer:
    """Cet agent prend toujours une décision aléatoire.
    Il dispose de deux fonction :
    totalRandom qui joue complétement au hasard,
    smartRandom qui prend une decision au hasard parmis celle possible."""
        
    def totalRandom():
        """Prend une decision complètement au hasard"""
        x = randrange(4)
        y = randrange(4)
        return x,y
    totalRandom = staticmethod(totalRandom)
    
    def smartRandom(self,listeActionPossible):
        """Prend une decision parmis celles possibles"""
        return choice(listeActionPossible)
    
    def nouvellePartie(self):
        pass

    def perdre(self):
        pass

    def gagner(self):
        pass

    def egaliser(self):
        pass

    def faireUnChoix(self,etat,liste_action_possible,tauxHasard=0.0,action_legal_seulement=False):
        return self.smartRandom(liste_action_possible)
