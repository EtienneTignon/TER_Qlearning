#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 22:19:53 2019

@author: ettignon
"""

import random

class QLearning:
    """Un algorithme de Q-learning. Adapté pour le puissance 4 en 3D (4x4x4).\n
    Cet IA ne fonctionne qu'avec des états sous la forme de matrice 4x4x4.
    Elle agrège les états sous la forme d'une matrice 2x2x2."""
    
    def __init__(self):
        self.transitionMatrice = {}
        self.ancienneAction = ()
        self.alpha = 0.3
        self.gamma = 0.2
        
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
        i = 0
        while(i<4):
            j = 0
            while(j<4):
                colone[(i,j)] = valeur
                j += 1
            i += 1
        self.transitionMatrice[etat] = colone
    
    def _choisirActionColone(self, actionPossible, etat):
        maxValeur = -1.0
        listActionChoisi = []
        actionChoisi = (-1,-1)
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
        etat = self._alterEtat(etat)
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
        etat = self._alterEtat(etat)
        # etat = etat.reshape(64)
        # etat = tuple(etat)
        if tuple(etat) not in list(self.transitionMatrice.keys()):
            self._ajouterColone(etat,1.0)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],1.0,etat)
        
    def perdu(self, etat):
        """Cette méthode est à appeler quand l'IA perd. Celà lui permet de le savoir et de mettre à jours sa matrice en conséquence.\n
        Elle prend comme argument l'état final du jeu."""
        etat = self._alterEtat(etat)
        # etat = etat.reshape(64)
        # etat = tuple(etat)
        if tuple(etat) not in list(self.transitionMatrice.keys()):
            self._ajouterColone(etat,0.0)
        if(not self.ancienneAction == ()):
            pastEtat, pastAction = self.ancienneAction
            self.transitionMatrice[pastEtat][pastAction] = self._MaJ(self.transitionMatrice[pastEtat][pastAction],0.0,etat)  
    
    def _alterEtat(self,etat):
        Etat = []
        #Zone 1
        if(etat[0][0][0]!=0 or etat[0][0][1]!=0 or etat[0][1][0]!=0 or etat[0][1][1]!=0 or etat[1][0][0]!=0 or etat[1][0][1]!=0 or etat[1][1][0]!=0 or etat[1][1][1]!=0):
            newEtat = 0
            i = 0
            while(i<2):
                j = 0
                while(j<2):
                    k = 0
                    while (k<2):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 2
        if(etat[0][0][2]!=0 or etat[0][0][3]!=0 or etat[0][1][2]!=0 or etat[0][1][3]!=0 or etat[1][0][2]!=0 or etat[1][0][3]!=0 or etat[1][1][2]!=0 or etat[1][1][3]!=0):
            newEtat = 0
            i = 0
            while(i<2):
                j = 0
                while(j<2):
                    k = 2
                    while (k<4):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 3
        if(etat[0][2][0]!=0 or etat[0][2][1]!=0 or etat[0][3][0]!=0 or etat[0][3][1]!=0 or etat[1][2][0]!=0 or etat[1][2][1]!=0 or etat[1][3][0]!=0 or etat[1][3][1]!=0):
            newEtat = 0
            i = 0
            while(i<2):
                j = 2
                while(j<4):
                    k = 0
                    while (k<2):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 4
        if(etat[0][2][2]!=0 or etat[0][2][3]!=0 or etat[0][3][2]!=0 or etat[0][3][3]!=0 or etat[1][2][2]!=0 or etat[1][2][3]!=0 or etat[1][3][2]!=0 or etat[1][3][3]!=0):
            newEtat = 0
            i = 0
            while(i<2):
                j = 2
                while(j<4):
                    k = 2
                    while (k<4):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 5
        if(etat[2][0][0]!=0 or etat[2][0][1]!=0 or etat[2][1][0]!=0 or etat[2][1][1]!=0 or etat[3][0][0]!=0 or etat[3][0][1]!=0 or etat[3][1][0]!=0 or etat[3][1][1]!=0):
            newEtat = 0
            i = 2
            while(i<4):
                j = 0
                while(j<2):
                    k = 0
                    while (k<2):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 6
        if(etat[2][0][2]!=0 or etat[2][0][3]!=0 or etat[2][1][2]!=0 or etat[2][1][3]!=0 or etat[3][0][2]!=0 or etat[3][0][3]!=0 or etat[3][1][2]!=0 or etat[3][1][3]!=0):
            newEtat = 0
            i = 2
            while(i<4):
                j = 0
                while(j<2):
                    k = 2
                    while (k<4):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 7
        if(etat[2][2][0]!=0 or etat[2][2][1]!=0 or etat[2][3][0]!=0 or etat[2][3][1]!=0 or etat[3][2][0]!=0 or etat[3][2][1]!=0 or etat[3][3][0]!=0 or etat[3][3][1]!=0):
            newEtat = 0
            i = 2
            while(i<4):
                j = 2
                while(j<4):
                    k = 0
                    while (k<2):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        #Zone 8
        if(etat[2][2][2]!=0 or etat[2][2][3]!=0 or etat[2][3][2]!=0 or etat[2][3][3]!=0 or etat[3][2][2]!=0 or etat[3][2][3]!=0 or etat[3][3][2]!=0 or etat[3][3][3]!=0):
            newEtat = 0
            i = 2
            while(i<4):
                j = 2
                while(j<4):
                    k = 2
                    while (k<4):
                        if(etat[i][j][k] == 1):
                            newEtat += 1
                        elif(etat[i][j][k] == 2):
                            newEtat -= 1                            
                        k += 1
                    j += 1
                i += 1
            if(newEtat == 0):
                Etat.append(3)
            elif(newEtat > 0):
                Etat.append(1)
            elif(newEtat < 0):
                Etat.append(2)
        else:
            Etat.append(0)
        return tuple(Etat)