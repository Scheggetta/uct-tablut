class Node:
    def __init__(self, state, action_performed, parent_node, depth):
        self.__state = state
        # `action_performed` is initialized if the node is not the root
        self.__action_performed = action_performed
        self.__parent_node = parent_node
        self.__depth = depth

        # total visits
        self.__n = 0
        # total rewards
        self.__v = 0

        self.__children = []
        self.__untried_moves = self.__state.get_moves()

    @property
    def state(self):
        return self.__state

    @property
    def action_performed(self):
        return self.__action_performed

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
    def untried_moves(self):
        return self.__untried_moves

    def add_child(self, child, action):
        assert action in self.__untried_moves

        self.children.append(child)
        self.untried_moves.remove(action)

        return child

    def __update(self, reward):
        self.n += 1
        self.v += reward

    def back_propagate(self, root_node, rewards, winner):
        player = self.state.get_player()

        if player == winner:
            self.__update(rewards[1])  # this node is bad for the parent
        elif player == (3 - winner):
            self.__update(rewards[0])  # this node is good for the parent
        else:
            self.__update(rewards[2])  # no player has won (draw)

        if tree_stats and values and (self == root_node):
            return values

        if not (self == root_node):
            if tree_stats and (self.__parent_node == root_node):
                move = self.__move
                n = self.__n
                v = self.__v
                q = v / n
                values = [move, q, v, n]

            return self.__parent_node.back_propagate(root_node, rewards, winner, tree_stats, values)
