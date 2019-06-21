# TER Q learning

Ce dépot contient une implémentation du puissance 4 en 3d, ainsi que plusieurs algorithmes de Q-Learning.

## Jeux implémentés
 - Connect43D.py : Ce fichier contient une implémentation du puissance 4 3D sur une grille 4x4x4. Il est néanmoins possible de paramétrer la taille de la grille et le nombre de pièces à aligner afin de travailler sur des variantes (comme le tic tac toe, le puissance 4 ...)

## IAs implémentées
 - IA\_random.py : Une IA complétement aléatoire.
 - IA\_qlearning.py : Une implémentation du Q-Learning généraliste.
 - IA\_qlearning\_c43d.py : Une implémentation du Q-Learning dédié au puissance 4 en 3D. Elle utilise une fonction de réduction pour limiter le nombre d'états. Elle est néanmoins peu efficace.
 - IA\_deepqlearning.py : Une implementation du deep Q learning composé uniquement de couches linéaires
 - IA\_deepqlearning\_conv.py : Une implementation du deep Q learning avec une couche de convolution supplémentaire

## Fichiers de test
 - Test\_C43D.py : Ce fichier test est paramétrable. Il est possible de choisir quels agents serons en copetition, sur quel jeu et avec quel hyper-paramètres.
