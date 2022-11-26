import argparse

from server_connector import ServerConnector
import converter as conv
from node import Node
from player import Player
from tree import Tree


def is_server_down(_server_turn) -> bool:
    return _server_turn not in map(lambda _turn: _turn.value, Player.__members__.values())


def receive_state():
    raw_state = conn.read()
    state = conv.convert_state(raw_state)
    _server_turn = conv.from_string_to_turn(conv.from_byte_to_string(raw_state))
    return state, _server_turn


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='SPTeam-tablut',
                                     description='Artificial intelligence agent that plays tablut')
    parser.add_argument('player', type=lambda s: s.upper())
    parser.add_argument('timeout', help='Timeout value in seconds ranging from 3 to 10000')
    parser.add_argument('ip_address')

    args = parser.parse_args()
    turn = Player.get_turn(args.player)

    # checks
    if not 3 <= int(args.timeout) <= 10000:
        raise ValueError('Timeout ranges from 3 to 10000')

    conn = ServerConnector(ip_address=args.ip_address, port=Player.port(turn))
    conn.send_msg(conv.convert_team_name('SPTeam'))

    if turn == Player.W:
        initial_state = conv.convert_state(conn.read())
    else:
        conn.read()
        initial_state = conv.convert_state(conn.read())

    print(initial_state)

    root_node = Node(state=initial_state,
                     action_performed=None,
                     turn=turn,
                     parent_node=None,
                     depth=0)
    tree = Tree(root_node=root_node, ucb_constant=1.5)
    current_state = tree.root_node.state

    while not current_state.is_terminal(turn):
        best_action, iter_n = tree.uct(timeout=int(args.timeout) - 2)

        print('UCT iterations: %d\n' % iter_n)

        # send action
        conn.send_msg(conv.convert_action(best_action, turn=turn))

        intermediate_state, server_turn = receive_state()
        print('Current state after our action (%s):' % best_action)
        print(intermediate_state)

        if is_server_down(server_turn):
            print('Match ended!')
            break

        current_state, server_turn = receive_state()
        print('Current state after enemy action:')
        print(current_state)

        if is_server_down(server_turn):
            print('Match ended!')
            break

        tree.update_root(intermediate_state, current_state)
