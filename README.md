# TER Q learning

Ce dépot contient une implémentation du puissance 4 en 3d et du morpion, ainsi que plusieurs algorithmes de Q-Learning et de MCTS.

## Jeux implémentés
 - Connect43D.py : Ce fichier contient une implémentation du puissance 4 3D sur une grille 4x4x4.
 - Morpion.py : Une implémentation du morpion.

## IAs implémentées
 - IA\_mcts.py : le Monté-Carlo Tree Search
 - IA\_qlearning\_v1.py : Une implémentation du Q-Learning dédié au puissance 4 en 3D.
 - IA\_qlearning\_v2.py : Une implémentation du Q-Learning prenant des matrices en entrées.
 - IA\_qlearning\_v3.py : Une implémentation du Q-Learning prenant des tuples en entrées.
 - IA\_random.py : Une IA complétement aléatoire.
 - IA\_deepqlearning.py : Une implementation du deep Q learning (!!!WIP!!!)

## Fichiers de test
 - test\_C43D\_Q.py
 - test\_C43D\_QvsMCTS.py
 - test\_C43D\_random.py
 - test\_morpion\_Q.py

## Deep Learning
 - DeepQTest.py : Contient un morpion et un agent de deep Q learning adapté pour le résoudre.
