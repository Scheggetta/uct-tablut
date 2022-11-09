from enum import Enum


class Players(Enum):
    W = 'WHITE'
    B = 'BLACK'

    @staticmethod
    def port(player):
        if player == Players.W:
            return 5800
        else:
            return 5801
