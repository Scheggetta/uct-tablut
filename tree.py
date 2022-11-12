import math
import random

from env import Env
from node import Node
from player import Player


class Tree:
    def __init__(self, root_node, ucb_constant):
        self.__root_node = root_node
        self.__ucb_constant = ucb_constant

    @property
    def root_node(self):
        return self.__root_node

    @property
    def ucb_constant(self):
        return self.__ucb_constant

    def ucb(self, parent_node: Node, child_node: Node) -> float:
        # q value (action value) of child_node
        q = child_node.v / child_node.n

        exploration_value = math.sqrt(math.log(parent_node.n) / child_node.n)

        return q + self.ucb_constant * exploration_value

    def uct(self, turn, iterations):
        root_node: Node = self.root_node

        for iteration_number in range(iterations):
            current_node = root_node

            # 1) selection
            # Move down the tree by choosing the node that every time has the maximum value of UCB formula until a node
            # is not fully expanded or is terminal
            while len(current_node.untried_actions) == 0 and not current_node.state.is_terminal(turn):
                current_node = max(current_node.children, key=lambda child: self.ucb(current_node, child))

            # 2) expansion
            is_terminal = current_node.state.is_terminal(turn)

            if not is_terminal:
                random_action = random.choice(current_node.untried_actions)
                current_state = Env.transition_function(current_node.state, random_action, turn)

                depth = current_node.depth
                current_turn = Player.next_turn(turn)
                new_node = Node(current_state, random_action, current_turn, current_node, depth + 1)
                current_node = current_node.add_child(new_node, random_action)

                # 3) rollout
                # current_state = current_state.clone()

                # available_actions = Env.get_available_actions(current_state, current_turn)
                while not current_state.is_terminal(current_turn):
                    available_actions = Env.get_available_actions(current_state, current_turn)
                    current_state = Env.transition_function(current_state, random.choice(available_actions),
                                                            current_turn)
                    current_turn = Player.next_turn(current_turn)
                    # available_actions = Env.get_available_actions(current_state, current_turn)

            # 4) backpropagation, now current_state is the terminal current_state
            rewards = [current_state.get_reward_of_winner(), current_state.get_reward_of_loser(), current_state.get_reward_of_draw()]
            winner = current_state.get_winner()
            current_node.back_propagate(root_node, rewards, winner)
