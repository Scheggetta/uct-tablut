import env
from player import Player
from setlist import SetList


class State:
    def __init__(self, whites: SetList, blacks: SetList, king: tuple):
        self.__s = [whites, blacks, king]

    def is_terminal(self, turn: Player) -> bool:
        return self.king is None or self.king in env.Env.king_escapes or \
               len(env.Env.get_available_actions(self, turn)) == 0

    def winner(self, turn: Player) -> Player:
        if self.king is None:
            return Player.B
        if self.king in env.Env.king_escapes:
            return Player.W
        if len(env.Env.get_available_actions(self, turn)) == 0:
            return Player.next_turn(turn)

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

    def checkers(self, turn: Player) -> SetList:
        return self.whites + [self.king] if turn == Player.W else self.blacks

    def __str__(self):
        # TODO: refactor
        board = [[0 for _ in range(9)] for _ in range(9)]
        mappings = {0: 'W', 1: 'B', 2: 'K'}
        king_died = False
        for k, lst in enumerate([self.whites, self.blacks, [self.king]]):
            if lst is None:
                king_died = True
                continue
            for i, j in lst:
                board[j-1][i-1] = mappings.get(k, 'k')

        res = '\n'.join([' '.join(map(str, i)) for i in board]) + '\n'
        if king_died:
            res += 'king died!\n'

        return res
