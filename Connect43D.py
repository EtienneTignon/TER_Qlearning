import numpy as np

class Connect43D:
    def __init__(self, z=4, y=4, x=4):
        self.game = np.full((z, y, x), 0, dtype=np.dtype('i8'))
        self.higher_level = np.full((y, x), 0, dtype=np.dtype('i8'))
        self.winner = 0
        self.actual_player = 1

    def _check_win(self, line):
        """ check one line if 4 same number are in the row"""
        total = 0
        if len(line) >= 4:
            for i in range(len(line)):
                if line[i] == self.actual_player:
                    total += 1
                    if total == 4:
                        self.winner = self.actual_player
                        break
                else:
                    total = 0

        return total == 4

    def _get_diagonal(self, matrix, x, y):
        """ get a diagonal from a matrix via diagonal function from numpy """
        if x == y:
            return matrix.diagonal()
        elif x > y:
            return matrix.diagonal(x - y)
        elif y > x:
            return matrix.diagonal(- (y - x))

    def _get_diagonals(self, z, y, x):
        """ get all the diagonals from a point in the tensor """
        left_x = x
        top_y = y
        right_x = self.game.shape[2] - x - 1
        bot_y = self.game.shape[1] - y - 1

        diagonals = []

        # z straight
        diagonals.append(self._get_diagonal(self.game[:, :, left_x], top_y, z))
        diagonals.append(self._get_diagonal(
            np.rot90(self.game, 1, axes=(2, 1))[:, :, bot_y], left_x, z))
        diagonals.append(self._get_diagonal(
            np.rot90(self.game, 2, axes=(2, 1))[:, :, right_x], bot_y, z))
        diagonals.append(self._get_diagonal(
            np.rot90(self.game, 3, axes=(2, 1))[:, :, top_y], right_x, z))

        # TODO : z diagonal

        return diagonals

    def do_move(self, move):
        """ apply a move for a player, and check if this is a winning move """
        x, y = move

        self.game[self.higher_level[y, x], y, x] = self.actual_player

        lines = []
        # x y straight
        lines.append(self.game[self.higher_level[y, x], y, :])
        lines.append(self.game[self.higher_level[y, x], :, x])
        lines.append(self.game[:, y, x])

        # x y diagonal
        lines.append(self._get_diagonal(
            self.game[self.higher_level[y, x], :, :], x, y))
        lines.append(self._get_diagonal(
            self.game[self.higher_level[y, x], :, :], x, y))
        lines.append(self._get_diagonal(np.rot90(
            self.game[self.higher_level[y, x], :, :]), self.game.shape[1] - 1 - y, x))

        # z
        lines += self._get_diagonals(self.higher_level[y, x], y, x)

        for line in lines:
            if self._check_win(line):
                break

        self.higher_level[y][x] += 1

        if self.actual_player == 1:
            self.actual_player = 2
        else:
            self.actual_player = 1

    def is_finished(self):
        return self.get_move() == [] or self.winner != 0

    def get_move(self):
        """ returns all the possible moves in the actual state of the game """
        return [(x, y) for y in range(self.higher_level.shape[0]) for x in range(self.higher_level.shape[1]) if self.higher_level[y][x] < self.game.shape[0]]
