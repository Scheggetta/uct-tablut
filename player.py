from enum import Enum


class Player(Enum):
    W = 'WHITE'
    B = 'BLACK'

    @staticmethod
    def next_turn(player):
        return Player.W if player == Player.B else Player.B

    @staticmethod
    def port(player):
        if player == Player.W:
            return 5800
        else:
            return 5801
