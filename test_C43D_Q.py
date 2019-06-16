#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:14:37 2019

@author: ettignon
"""

from Connect43D import Connect43D 
from IA_qlearning_v2 import QLearning
from IA_random import RandomPlayer

def partieEntreQ(joueur1, joueur2):
    i = 0
    gagne = 0.0
    egualise = 0.0
    perd = 0.0
    while i < 100:
        game = Connect43D(1,3,3,3)
        while True:  
            #if i==99: print(game.game)
            if (game.is_finished()):
                break
            game.do_move(joueur1.prendreUneDecision(game.game,game.get_move(),0.0))
            #if i==99: print(game.game)
            if (game.is_finished()):
                break
            game.do_move(joueur2.prendreUneDecision(game.game,game.get_move(),0.0))
        if(game.winner == 1):
            joueur1.gagne()
            joueur2.perdu()
            gagne += 1.0
        elif(game.winner == 2):
            joueur1.perdu()
            joueur2.gagne()
            perd += 1.0
        else:
            joueur1.egalite()
            joueur2.egalite()
            egualise += 1.0
        i += 1
    ratioj1 = gagne/100.0
    rationul = egualise/100.0
    ratioj2 = perd/100.0
    return ratioj1,rationul,ratioj2

def EntrainementEntreQ(joueur1, joueur2):
    i = 0
    while i < 1:
        game = Connect43D(1,3,3,3)
        while True:    
            if (game.is_finished()):
                break
            game.do_move(joueur1.prendreUneDecision(game.game,game.get_move(),(1.0/(i+1))))
            if (game.is_finished()):
                break
            game.do_move(joueur2.prendreUneDecision(game.game,game.get_move(),(1.0/(i+1))))
        if(game.winner == 1):
            joueur1.gagne()
            joueur2.perdu()
        elif(game.winner == 2):
            joueur1.perdu()
            joueur2.gagne()
        else:
            joueur1.egalite()
            joueur2.egalite()
        i += 1

def partieContreRand(joueur, premier): 
    joueurRand = RandomPlayer()
    i = 0
    gagne = 0.0
    partie = 100.0
    while i < partie:
        game = Connect43D()
        if(not premier):
            game.do_move(joueurRand.smartRandom(game.get_move()))
        while True:
            if (game.is_finished()):
                break
            game.do_move(joueur.prendreUneDecision(game.game,game.get_move(),0.0))
            if (game.is_finished()):
                break
            game.do_move(joueurRand.smartRandom(game.get_move()))
        if(premier):
            if(game.winner == 1):
                joueur.gagne()
                gagne += 1.0
            else:
                joueur.perdu()
        else:
            if(game.winner != 1):
                joueur.gagne()
                gagne += 1.0
            else:
                joueur.perdu()   
        i += 1
    ratio = gagne/partie
    if(not premier):
        ratio = 1.0-ratio
    return ratio

def entrainementContreRand(joueur, premier): 
    joueurRand = RandomPlayer()
    i = 0
    gagne = 0.0
    while i < 100:
        game = Connect43D()
        if(not premier):
            game.do_move(joueurRand.smartRandom(game.get_move()))
        while True:
            if (game.is_finished()):
                break
            game.do_move(joueur.prendreUneDecision(game.game,game.get_move(),(1.0/(i+1))))
            if (game.is_finished()):
                break
            game.do_move(joueurRand.smartRandom(game.get_move()))
        if(premier):
            if(game.winner == 1):
                joueur.gagne()
                gagne += 1.0
            else:
                joueur.perdu()
        else:
            if(game.winner != 1):
                joueur.gagne()
                gagne += 1.0
            else:
                joueur.perdu()            
        i += 1
    ratio = gagne/100.0
    if(not premier):
        ratio = 1.0-ratio
    return ratio

"""
i = 0
gagne = 0
while i < 100:
    print("Partie : ", i)
    game = Connect43D()
    while True:    
        if (game.is_finished()):
            break
        game.do_move(joueurQ.prendreUneDecision(game.game,game.get_move()))
        if (game.is_finished()):
            break
        game.do_move(joueurRand.smartRandom(game.get_move()))
    if(game.winner == 1):
        joueurQ.gagne(game.game)
        gagne += 1
    else:
        joueurQ.perdu(game.game)
    print("Victoire : ", gagne)
    i += 1

joueurQ1 = QLearning()
joueurQ2 = QLearning()



i = 0
gagne1 = 0
gagne2 = 0
while i < 1000:
    print("Partie : ", i)
    game = Connect43D()
    while True:    
        if (game.is_finished()):
            break
        game.do_move(joueurQ1._decisionRationel(game.game,game.get_move()))
        if (game.is_finished()):
            break
        game.do_move(joueurQ2._decisionRationel(game.game,game.get_move()))
    if(game.winner == 1):
        joueurQ1.gagne(game.game)
        joueurQ2.perdu(game.game)
        gagne1 += 1
    else:
        joueurQ1.perdu(game.game)
        joueurQ2.gagne(game.game)
        gagne2 += 1
    print("Victoire : ", gagne1, " - ", gagne2)
    i += 1
    
joueurQ1.enrengistrerMatriceTransition("Q1.txt")
joueurQ2.enrengistrerMatriceTransition("Q2.txt")
"""

"""
mon_fichier = open("Resultat.txt", "w")
alpha1 = 0.0
while(alpha1 <= 0.9):
    alpha2 = alpha1 + 0.1
    while(alpha2 <= 1):
        gamma1 = 0.0
        while(gamma1 <= 0.9):
            gamma2 = gamma1 + 0.1
            while(gamma2 <= 1):
                txt = "[IA1 : alpha=" + str(alpha1) + ", gamma=" + str(gamma1) + "][IA2 : alpha=" + str(alpha2) + ", gamma=" + str(gamma2) + "]\n"
                #Competition IA1 vs IA2
                joueurQ1 = QLearning()
                joueurQ1.alpha = alpha1
                joueurQ1.gamma = gamma1
                joueurQ2 = QLearning()
                joueurQ2.alpha = alpha2
                joueurQ2.gamma = gamma2
                resultat = partieEntreQ(joueurQ1, joueurQ2)
                txt += ">IA1 vs IA2 : " + str(resultat) + "\n"
                #Competition IA2 vs IA1
                joueurQ1 = QLearning()
                joueurQ1.alpha = alpha1
                joueurQ1.gamma = gamma1
                joueurQ2 = QLearning()
                joueurQ2.alpha = alpha2
                joueurQ2.gamma = gamma2
                resultat = partieEntreQ(joueurQ2, joueurQ1)
                txt += ">IA2 vs IA1 : " + str(resultat) + "\n"
                #Competition IA1 vs Rand
                joueurQ1 = QLearning()
                joueurQ1.alpha = alpha1
                joueurQ1.gamma = gamma1
                ratio1 = partieContreRand(joueurQ1,True)
                txt += ">IA1 vs Rand : " + str(ratio1) + "\n"
                #Competition Rand vs IA1
                joueurQ1 = QLearning()
                joueurQ1.alpha = alpha1
                joueurQ1.gamma = gamma1
                ratio2 = partieContreRand(joueurQ1,False)
                txt += ">Rand vs IA1 : " + str(ratio2) + "\n\n"
                #fin des test
                if(maxrat < (ratio1+ratio2)):
                    bestalpha = alpha1
                    bestgamma = gamma1
                print(txt)
                mon_fichier.write(txt)
                gamma2 += 0.1
            gamma1 += 0.1
        alpha2 += 0.1
    alpha1 += 0.1
"""  
"""
maxrat = 0.0
bestalpha = 0.0
bestgamma = 0.0
alpha = 0.1
while(alpha<=1):
    gamma = 0.0
    while(gamma<=1):
        txt = "[IA1 : alpha=" + str(alpha) + ", gamma=" + str(gamma) + "]\n"
        #Competition IA1 vs Rand
        joueurQ1 = QLearning()
        joueurQ1.alpha = alpha
        joueurQ1.gamma = gamma
        entrainementContreRand(joueurQ1,True)
        print(joueurQ1.alpha)
        print(joueurQ1.gamma)
        ratio1 = partieContreRand(joueurQ1,True)
        txt += ">IA1 vs Rand : " + str(ratio1) + "\n"
        #Competition Rand vs IA1
        joueurQ1 = QLearning()
        joueurQ1.alpha = alpha
        joueurQ1.gamma = gamma
        entrainementContreRand(joueurQ1,False)
        ratio2 = partieContreRand(joueurQ1,False)
        txt += ">Rand vs IA1 : " + str(ratio2) + "\n\n"
        #fin des test
        if(maxrat < (ratio1+ratio2)):
            maxrat = (ratio1+ratio2)
            bestalpha = alpha
            bestgamma = gamma
        print(txt)
        joueurQ1.enrengistrerMatriceTransition("test.txt")
        gamma+=0.09
    alpha+=0.09             
"""

joueurQ = QLearning()
joueurQ2 = QLearning()
i = 0
while(i<1000):
    EntrainementEntreQ(joueurQ,joueurQ2)
    print(partieEntreQ(joueurQ,joueurQ2))
    # joueurQ.enrengistrerMatriceTransition("test.txt")
    i += 1