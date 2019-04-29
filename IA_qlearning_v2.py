#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:26:13 2019

@author: ettignon
"""

import random
import numpy as np

class QLearning:
    """Un algorithme de Q-learning.\n
    Cet IA fonctionne normalement avec des états sous la forme de matrice.
    Attention ! Elle rajoutera des états à l'infini si necessaire."""
    
    def __init__(self):
        self.transitionMatrice = {}
        self.ancienneAction = ()
        self.alpha = 0.1
        self.gamma = 0.3
        
    def afficherMatriceTransition(self):
        """Cette méthode permet d'afficher la matrice de transition dans le terminal."""
        for etat, action in self.transitionMatrice.items():
            print("Pour l'état : ", etat)
            print(action)
    
    def enrengistrerMatriceTransition(self, nomFichier):
        """Cette méthode permet d'enrengistrer la matrice de transition dans un fichier.\n
        Elle prend en paramètre le nom du fichier dans lequel écrire.\n
        Si le fichier n'éxiste pas, il sera créé. S'il existe déjà, son ancien contenu sera effacé."""
        mon_fichier = open(nomFichier, "w")
        for etat, action in self.transitionMatrice.items():
            mon_fichier.write("Pour l'état : " + str(etat) + "\n" + str(action) + "\n\n")
        mon_fichier.close()
            
    def _ajouterColone(self,etat, valeur):
        colone = {}
        self.transitionMatrice[etat] = colone
    
    def _choisirActionColone(self, actionPossible, etat):
        maxValeur = -1.0
        listActionChoisi = []
        listActionNonRencontré = []
        for indice, action in enumerate(actionPossible):
            if action not in self.transitionMatrice[etat].keys():
                listActionNonRencontré.append(action)
        if listActionNonRencontré != []:
            actionChoisi = random.choice(listActionNonRencontré)
            self.transitionMatrice[etat][actionChoisi] = 0.5
            return actionChoisi
        for action, valeur in self.transitionMatrice[etat].items():
            if action in actionPossible:
                if valeur == maxValeur:
                    listActionChoisi.append(action)
                if valeur > maxValeur:
                    listActionChoisi = [action]
                    maxValeur = valeur
        if(listActionChoisi != []):
            actionChoisi = random.choice(listActionChoisi)
        return actionChoisi
    
    def _maxColone(self, etat):
        maxValeur = -1.0
        for action, valeur in self.transitionMatrice[etat].items():
            if valeur > maxValeur:
                maxValeur = valeur
        return maxValeur
    
    def _MaJ(self, ancienneValeur, recompense, etatSuivant):
        maxNouvelleValeur = self._maxColone(etatSuivant)
        newValeur = ((1.0-self.alpha)*ancienneValeur)+(self.alpha*(recompense+(self.gamma*maxNouvelleValeur)))
        # print(newValeur)
        return (newValeur)
    
    def _decisionRationel(self, etat, actionPossible):
        actionChoisi = self._choisirActionColone(actionPossible, etat)
        return actionChoisi
    
    def prendreUneDecision(self, etat, actionPossible, tauxExploration):
        """Cette méthode sers à faire prendre une decision à l'IA.\n
        Le premier argument est l'état actuel du plateau de jeu.\n
        Le deuxième argument est la liste des actions que peux prendre l'IA.\n
        Le troixième est un taux d'exploration. Plus il est fort, plus l'IA explorera en prenant une decision aléatoire. (Si l'argument vaut 1.0, la decision sera toujours aléatoire). 
        Plus il est faible, plus l'IA priviligiera la meilleur action connu. (Si l'argument vaut 0.0, l'IA prendra à coup sur la meilleur décision selon elle)."""
        etatnp = np.matrix(etat)
        etat = etat.reshape(etatnp.size)
        etat = tuple(etat)
        if etat not in list(self.transitionMatrice.keys()):
            self._ajouterColone(etat,0.5)
        if (random.random()<tauxExploration):
            actionChoisi = self._decisionRationel(etat, actionPossible)
        else:
            actionChoisi = random.choice(actionPossible)
        if(self.ancienneAction != ()):
            pastEtat, pastAction = self.ancienneAction
            self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],0.5,etat)  
        self.ancienneAction = (etat, actionChoisi)   
        return actionChoisi
    
    def gagne(self, etat):
        """Cette méthode est à appeler quand l'IA gagne. Celà lui permet de le savoir et de mettre à jours sa matrice en conséquence.\n
        Elle prend comme argument l'état final du jeu."""
        etatnp = np.matrix(etat)
        etat = etat.reshape(etatnp.size)
        etat = tuple(etat)
        if etat not in list(self.transitionMatrice.keys()):
            self._ajouterColone(etat,1.0)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],1.0,etat)
        
    def perdu(self, etat):
        """Cette méthode est à appeler quand l'IA perd. Celà lui permet de le savoir et de mettre à jours sa matrice en conséquence.\n
        Elle prend comme argument l'état final du jeu."""
        etatnp = np.matrix(etat)
        etat = etat.reshape(etatnp.size)
        etat = tuple(etat)
        if etat not in list(self.transitionMatrice.keys()):
            self._ajouterColone(etat,0.0)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],0.0,etat)  