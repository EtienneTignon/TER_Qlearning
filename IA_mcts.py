from math import sqrt, log
import numpy as np
from random import choice
from copy import deepcopy
#import networkx as nx
#import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import time
#import cProfile
from multiprocessing import Process, Pool
from Connect43D import Connect43D

class Node:
    global_id = 0

    def __init__(self, state, move=None):
        self.id = Node.global_id
        Node.global_id += 1

        self.parent = None
        self.children = []
        self.untriedMove = state.get_move()

        self.win = 0
        self.visited = 0

        self.player = 0
        self.move = move

    def is_leaf(self):
        return self.children == []

    def is_root(self):
        return self.parent == None

    def add_child(self, move, state):
        child = Node(state, move)
        child.parent = self
        self.untriedMove.remove(move)
        self.children.append(child)
        return child

    def select_best_child(self, e=1.0):
        return sorted(self.children, key=lambda c: c.win / c.visited + e * sqrt(2 * log(self.visited) / c.visited))[-1]


def backpropagation(node, state, player):
    while not node.is_root():
        if state.winner == player:
            node.win += 1
        elif state.winner == 0:
            node.win += 0.5
        node = node.parent

    if state.winner == player:
        node.win += 1
    elif state.winner == 0:
        node.win += 0.5

    return node


def rollout(init_state):
    state = deepcopy(init_state)
    while not state.is_finished():
        move = choice(state.get_move())
        state.do_move(move)
    return state.winner


def mcts_leaf_parallelization(init_state, max_iter, player, jobs=4, rollout_count=32):
    root = Node(init_state)

    Node.global_id = 0

    for iter in range(max_iter):
        node = root
        state = deepcopy(init_state)

        while not node.is_leaf() and node.untriedMove == []:
            node = node.select_best_child()
            state.do_move(node.move)

        if node.untriedMove != []:
            move = choice(node.untriedMove)
            state.do_move(move)
            node = node.add_child(move, state)

        winners = Parallel(jobs, "loky")(delayed(rollout)(
            state) for _ in range(rollout_count))

        #processes = []
        # for _ in range(jobs):
        #    p = Process(target=rollout, args=(state))
        #    p.start()
        #    processes.append(p)

        # for p in processes:
        #    p.join()

        #pool = Pool(processes=4)
        #winners = pool.map(rollout, [state for _ in range(4)])

        visited = rollout_count
        win_player = 0
        for win in winners:
            if win == player:
                win_player += 1
            elif win == 0:
                win_player += 0.5

        while not node.is_root():
            node.visited += visited
            node.win += win_player
            node = node.parent

        node.visited += 1
        if state.winner == player:
            node.win += 1.0
        elif state.winner == 0:
            node.win += 0.5

    return sorted(root.children, key=lambda c: c.visited)[-1].move


def mcts(init_state, max_iter, player, viz=False):
    root = Node(init_state)

    Node.global_id = 0

    time_selection = 0
    time_expansion = 0
    time_rollout = 0
    time_backpropagation = 0
    time_total = 0

    #g = None
    # if viz:
    #    g = nx.Graph()
    #    g.add_node(root.id)

    for iter in range(max_iter):
        node = root
        state = deepcopy(init_state)

        start_selection = time.time()
        while not node.is_leaf() and node.untriedMove == []:
            node = node.select_best_child()
            state.do_move(node.move)
        time_selection += time.time() - start_selection

        start_expansion = time.time()
        if node.untriedMove != []:
            move = choice(node.untriedMove)
            state.do_move(move)
            node = node.add_child(move, state)

            # if viz:
            #    g.add_node(node.id)
            #    g.add_edge(node.parent.id, node.id)
        time_expansion += time.time() - start_expansion

        start_rollout = time.time()
        while not state.is_finished():
            move = choice(state.get_move())
            state.do_move(move)
        # for i in range(20):
        #    if state.is_finished():
        #        break
        #    move = choice(state.get_move())
        #    state.do_move(move)
        time_rollout += time.time() - start_rollout

        start_backpropagation = time.time()
        while not node.is_root():
            node.visited += 1
            if state.winner == player:
                node.win += 1.0
            elif state.winner == 0:
                node.win += 0.5
            node = node.parent

        node.visited += 1
        if state.winner == player:
            node.win += 1.0
        elif state.winner == 0:
            node.win += 0.5
        time_backpropagation += time.time() - start_backpropagation

    # if viz:
    #    nx.draw(g, with_labels=True, font_weight='bold')
    #    plt.show()

    # print("================================")
    #print(f"selection : {time_selection}")
    #print(f"expansion : {time_expansion}")
    #print(f"rollout : {time_rollout}")
    #print(f"backpropagation : {time_backpropagation}")

    # return root.children
    return sorted(root.children, key=lambda c: c.visited)[-1].move
