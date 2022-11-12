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
        sym = {'white': u'●', 'black': u'◎', 'king': u'₻', 'castle': u'□', 'camp': u'□',
               'horizontal_wall': u'━', 'vertical_wall': u'┃', 'top_left': u'┏', 'top_right': u'┓',
               'bottom_left': u'┗', 'bottom_right': u'┛', 'empty': ' '}

        res = '    A B C D E F G H I\n  ' + sym['top_left'] + sym['horizontal_wall'] * 19 + sym['top_right'] + '\n'

        for row in range(1, 10):
            symbols = []
            for col in range(1, 10):
                cell = col, row
                if cell in self.whites:
                    symbols.append(sym['white'])
                elif cell == self.king:
                    symbols.append(sym['king'])
                elif cell in self.blacks:
                    symbols.append(sym['black'])
                elif cell == env.Env.castle:
                    symbols.append(sym['castle'])
                elif cell in env.Env.camps:
                    symbols.append(sym['camp'])
                else:
                    symbols.append(sym['empty'])

            line = ' ' + ' '.join(symbols) + ' '

            res += '%d ' % row + sym['vertical_wall'] + line + sym['vertical_wall'] + '\n'

        res += '  ' + sym['bottom_left'] + sym['horizontal_wall'] * 19 + sym['bottom_right']

        return res
