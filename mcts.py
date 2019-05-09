from math import sqrt, log
from copy import deepcopy
from random import choice
import time
import networkx as nx
import matplotlib.pyplot as plt
from joblib import Parallel, delayed


class Node:

    def __init__(self, state, move=None, parent=None):
        self.parent = parent
        self.children = []

        self.untriedMove = state.get_move()
        self.score = 0
        self.visit = 0

        self.move = move
        self.player = 3 - state.actual_player

    def is_leaf(self):
        return self.children == []

    def is_root(self):
        return self.parent == None

    def add_child(self, move, state):
        child = Node(state, move=move, parent=self)
        self.untriedMove.remove(move)
        self.children.append(child)
        return child

    def select_best_child(self, e=1.0):
        return sorted(self.children, key=lambda c: c.score / c.visit + e * sqrt(2 * log(self.visit) / c.visit))[-1]


def rollout(state):
    while not state.is_finished():
        state.do_move(choice(state.get_move()))
    return state.winner

def apply_mcts_root_parallelization(tree, init_state, player, agent, n_jobs=-1, root_count=32):
    trees = Parallel(n_jobs, "loky")(delayed(apply_mcts)(
        tree, init_state, player, agent, return_tree=True) for _ in range(root_count))

    agent.tree = trees[0]
    trees.remove(tree)

    for t in trees:
        for c in t.children:
            for r_c in tree.children:
                if c == r_c:
                    r_c.visited += c.visited
                    r_c.win += c.win

    return sorted(tree.children, key=lambda c: c.visit)[-1].move


def apply_mcts(tree, init_state, player, max_iter, jobs=-1, rollout_count=12):
    time_selection = 0
    time_expansion = 0
    time_rollout = 0
    time_backpropagation = 0
    time_total = 0
    #tree = Node(init_state)

    for iter in range(max_iter):
        node = tree
        state = deepcopy(init_state)

        # selection
        start_selection = time.time()
        while not node.is_leaf() and node.untriedMove == []:
            node = node.select_best_child()
            state.do_move(node.move)
        time_selection += time.time() - start_selection

        # expansion
        start_expansion = time.time()
        if node.untriedMove != []:
            move = choice(node.untriedMove)
            state.do_move(move)
            node = node.add_child(move, state)
        time_expansion += time.time() - start_expansion

        # rollout
        start_rollout = time.time()
        while not state.is_finished():
           move = choice(state.get_move())
           state.do_move(move)

        #winners = Parallel(jobs, "loky")(delayed(rollout)(
        #    state) for _ in range(rollout_count))

        #win_player_1 = 0
        #win_player_2 = 0
        #draw = 0

        #for win in winners:
        #    if win == 1:
        #       win_player_1 += 1
        #    elif win == 2:
        #        win_player_2 += 1
        #    else:
        #        draw += 1
            
        time_rollout += time.time() - start_rollout

        # backpropagation
        start_backpropagation = time.time()
        while node != None:
            node.visit += 1.0
            if state.winner == node.player:
                node.score += 1.0
            elif state.winner == 0:
                node.score += 0.5
            node = node.parent

        #while node != None:
        #    node.visit += rollout_count
        #    if state.winner == node.player == 1:
        #        node.score += win_player_1
        #    elif state.winner == node.player == 2:
        #        node.score += win_player_2        
        #    node = node.parent
        time_backpropagation += time.time() - start_backpropagation

    #print("=============== Total Time =================")
    #print(f"selection : {time_selection}")
    #print(f"expansion : {time_expansion}")
    #print(f"rollout : {time_rollout}")
    #print(f"backpropagation : {time_backpropagation}")

    #print(f"{player} : {[ c.score / c.visit for c in tree.children]}")
    return sorted(tree.children, key=lambda c: c.visit)[-1].move
    #return sorted(tree.children, key=lambda c: c.score/c.visit)[-1].move
