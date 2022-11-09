import math
import random

from node import Node


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

    def uct(self, player, iterations):
        root_node: Node = self.root_node

        for iteration_number in range(iterations):
            current_node = root_node

            # 1) selection
            # Move down the tree by choosing the node that every time has the maximum value of UCB formula until a node
            # is not fully expanded or is terminal
            while not current_node.untried_moves and current_node.children:
                current_node = max(current_node.children, key=lambda child: self.ucb(current_node, child))

            # 2) expansion
            state = current_node.get_state().clone()
            untried_moves = current_node.get_untried_moves()
            depth = current_node.get_depth()

            # if untried_moves is not empty, state is not terminal
            if untried_moves and depth != tree_depth:
                rand_move = untried_moves[random.randrange(0, len(untried_moves))]
                state = state.do_move(rand_move)
                depth = depth + 1
                current_node = current_node.add_child(Node(state, rand_move, current_node, depth), rand_move)

            # 3) rollout
            moves_done = 0
            state = state.clone()
            moves = state.get_moves()
            while moves:
                state = state.do_random_move(moves)
                moves = state.get_moves()
                moves_done += 1

            # 4) backpropagation, now state is the terminal state
            rewards = [state.get_reward_of_winner(), state.get_reward_of_loser(), state.get_reward_of_draw()]
            winner = state.get_winner()
            current_node.back_propagate(root_node, rewards, winner)
