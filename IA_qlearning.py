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
        maxValeur = -100.0
        listActionChoisi = []
        listActionNonRencontre = []
        for indice, action in enumerate(actionPossible):
            if action not in self.transitionMatrice[etat].keys():
                listActionNonRencontre.append(action)
        if listActionNonRencontre != []:
            actionChoisi = random.choice(listActionNonRencontre)
            self.transitionMatrice[etat][actionChoisi] = 0.0
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
    
    def faireUnChoix(self, etat, actionPossible, tauxHasard=0.0, action_legal_seulement=True):
        """Cette méthode sers à faire prendre une decision à l'IA.\n
        Le premier argument est l'état actuel du plateau de jeu.\n
        Le deuxième argument est la liste des actions que peux prendre l'IA.\n
        Le troixième est un taux d'exploration. Plus il est fort, plus l'IA explorera en prenant une decision aléatoire. (Si l'argument vaut 1.0, la decision sera toujours aléatoire). 
        Plus il est faible, plus l'IA priviligiera la meilleur action connu. (Si l'argument vaut 0.0, l'IA prendra à coup sur la meilleur décision selon elle)."""
        etat = np.array(etat)
        etat = etat.reshape(etat.size)
        etat = tuple(etat)
        if etat not in list(self.transitionMatrice.keys()):
            self._ajouterColone(etat,0.5)
        if (random.random()>tauxHasard):
            actionChoisi = self._decisionRationel(etat, actionPossible)
        else:
            actionChoisi = random.choice(actionPossible)
        if(self.ancienneAction != ()):
            pastEtat, pastAction = self.ancienneAction
            if pastAction in self.transitionMatrice[pastEtat]:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],0.0,etat)
            else:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(0.0,0.0,etat)
        self.ancienneAction = (etat, actionChoisi)   
        return actionChoisi
    
    def gagner(self):
        """Cette méthode est à appeler quand l'IA gagne. Celà lui permet de le savoir et de mettre à jours sa matrice en conséquence.\n
        Elle prend comme argument l'état final du jeu."""
        if ("Victoire") not in list(self.transitionMatrice.keys()):
            self._ajouterColone(("Victoire"),1.0)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            if pastAction in self.transitionMatrice[pastEtat]:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],1.0,("Victoire"))
            else:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(10.0,10.0,("Victoire"))
        
    def perdre(self):
        """Cette méthode est à appeler quand l'IA perd. Celà lui permet de le savoir et de mettre à jours sa matrice en conséquence.\n
        Elle prend comme argument l'état final du jeu."""
        if ("Defaite") not in list(self.transitionMatrice.keys()):
            self._ajouterColone(("Defaite"),0.0)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            if pastAction in self.transitionMatrice[pastEtat]:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],-10.0,("Defaite"))
            else:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(-10.0,-10.0,("Defaite"))

    def egaliser(self):
        """Cette méthode est à appeler quand l'IA égalise. Celà lui permet de le savoir et de mettre à jours sa matrice en conséquence.\n
        Elle prend comme argument l'état final du jeu."""
        if ("Egalité") not in list(self.transitionMatrice.keys()):
            self._ajouterColone(("Egalité"),0.5)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            if pastAction in self.transitionMatrice[pastEtat]:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],0.0,("Egalité"))
            else:
                self.transitionMatrice[pastEtat][pastAction] = self._MaJ(0.0,0.0,("Egalité"))
                
    def nouvellePartie(self):
        self.ancienneAction = ()