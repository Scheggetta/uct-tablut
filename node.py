from typing import Union

from action import Action
from env import Env
from player import Player
from state import State


class Node:
    def __init__(self, state: State, action_performed: Union[Action, None], turn: Player, parent_node, depth: int):
        # `action_performed` and `parent_node` are initialized if the node is not the root
        self.__state = state
        self.__action_performed = action_performed
        self.__turn = turn
        self.__parent_node = parent_node
        self.__depth = depth

        # total visits
        self.__n = 0
        # total rewards
        self.__v = 0

        self.__children = []
        self.__untried_actions = Env.get_available_actions(self.__state, self.__turn)

    @property
    def state(self):
        return self.__state

    @property
    def is_terminal(self):
        return self.state.is_terminal(self.turn)

    @property
    def action_performed(self):
        return self.__action_performed

    @property
    def turn(self):
        return self.__turn

    @property
    def parent_node(self):
        return self.__parent_node

    @property
    def depth(self):
        return self.__depth

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value

    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, value):
        self.__v = value

    @property
    def children(self):
        return self.__children

    @property
    def q(self):
        return self.v / self.n

    @property
    def untried_actions(self):
        return self.__untried_actions

    def add_child(self, child, action: Action):
        assert action in self.__untried_actions

        self.children.append(child)
        self.untried_actions.remove(action)

        return child

    def __update(self, reward):
        self.n += 1
        self.v += reward

    def backpropagate(self, winner):
        winner_reward = 1
        loser_reward = -1
        current_node = self

        while current_node is not None:
            # draw is not considered
            if current_node.turn == winner:
                current_node.__update(loser_reward)
            else:
                current_node.__update(winner_reward)
            current_node = current_node.parent_node
