import math
import random
import time
from typing import Union

from action import Action
from env import Env
from node import Node
from player import Player


class Tree:
    def __init__(self, root_node: Node, ucb_constant: Union[int, float]):
        self.__root_node = root_node
        self.__ucb_constant = ucb_constant

    @property
    def root_node(self):
        return self.__root_node

    @root_node.setter
    def root_node(self, value):
        self.__root_node = value

    '''
    def reset_root(self):
        best_node = max(self.root_node.children, key=lambda child: child.q)
        new_root_node = Node(state=best_node.state,
                             action_performed=None,
                             turn=best_node.turn,
                             parent_node=None,
                             depth=0)
        self.root_node = new_root_node
    '''

    @property
    def ucb_constant(self):
        return self.__ucb_constant

    def ucb(self, parent_node: Node, child_node: Node) -> float:
        # q value (action value) of child_node
        q = child_node.v / child_node.n

        exploration_value = math.sqrt(math.log(parent_node.n) / child_node.n)

        return q + self.ucb_constant * exploration_value

    def uct(self, timeout: Union[int, float]) -> Action:
        start_time = time.perf_counter()
        root_node: Node = self.root_node
        iter_n = 0

        while time.perf_counter() < start_time + timeout:
            iter_n += 1
            current_node = root_node

            # 1) selection
            # Move down the tree by choosing the node that every time has the maximum value of UCB formula until a node
            # is not fully expanded or is terminal
            while len(current_node.untried_actions) == 0 and not current_node.is_terminal:
                current_node = max(current_node.children, key=lambda child: self.ucb(current_node, child))

            # 2) expansion
            if not current_node.is_terminal:
                random_action = random.choice(current_node.untried_actions)
                current_state = Env.transition_function(current_node.state, random_action, current_node.turn)

                depth = current_node.depth
                current_turn = Player.next_turn(current_node.turn)
                new_node = Node(current_state, random_action, current_turn, current_node, depth + 1)
                current_node = current_node.add_child(new_node, random_action)

                # 3) rollout
                while not current_state.is_terminal(current_turn):
                    available_actions = Env.get_available_actions(current_state, current_turn)
                    current_state = Env.transition_function(current_state, random.choice(available_actions),
                                                            current_turn)
                    current_turn = Player.next_turn(current_turn)
            else:
                current_state = current_node.state
                current_turn = current_node.turn

            winner = current_state.winner(current_turn)

            # 4) backpropagation, now current_state is the terminal current_state
            current_node.backpropagate(winner)

        return max(root_node.children, key=lambda child: child.q).action_performed, iter_n
