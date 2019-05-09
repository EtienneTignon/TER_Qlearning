from mcts import Node, apply_mcts
from random import choice

class Agent:

    def __init__(self, player_id, game):
        self.player_id = player_id
        self.tree = Node(game)
        self.game = game

    def update_action(self, action):
        """ update the root tree, if the child doesn't exist it will be created """
        new_root = None
        for c in self.tree.children:
            if c.move == action:
                new_root = c
                new_root.parent = None
        if new_root == None:
            # create the new child
            new_root = Node(self.game)
        
        self.tree = new_root

    def next_action(self, max_iter, random=False):
        if random:
            return choice(self.game.get_move())
        return apply_mcts(self.tree, self.game, self.player_id, max_iter=max_iter)
