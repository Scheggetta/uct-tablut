from players import Players
from setlist import SetList


class State:
    def __init__(self, whites: SetList, blacks: SetList, king: tuple):
        self.__s = [whites, blacks, king]

    @property
    def s(self) -> list:
        return self.__s

    @property
    def whites(self) -> SetList:
        return self.s[0]

    @property
    def blacks(self) -> SetList:
        return self.s[1]

    @property
    def king(self) -> tuple:
        return self.s[2]

    @king.setter
    def king(self, value):
        self.s[2] = value

    def checkers(self, turn: Players) -> SetList:
        return self.whites + [self.king] if turn == Players.W else self.blacks

    def __str__(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        mappings = {0: 'W', 1: 'B', 2: 'K'}
        king_died = False
        for k, lst in enumerate([self.whites, self.blacks, [self.king]]):
            for i, j in lst:
                if (i, j) == (0, 0):
                    king_died = True
                else:
                    board[j-1][i-1] = mappings.get(k, 'k')

        res = '\n'.join([' '.join(map(str, i)) for i in board]) + '\n'
        if king_died:
            res += 'king died!\n'

        return res
