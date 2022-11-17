import argparse
import random

from server_connector import ServerConnector
import converter as conv
from node import Node
from player import Player
from tree import Tree

# TODO: speed improvements:
#       - deepcopy
#       - `get_available_actions` in `state.is_terminal(turn)`
#       -`SetList`

# TODO: UCT performance improvements:
#       - symmetry
#       - `tree.reset_root`

# TODO: terminate loop when game finishes

# TODO: deploy on VM

# Seed
random.seed(100)

parser = argparse.ArgumentParser(prog='SPTeam-tablut',
                                 description='Artificial intelligence agent that plays tablut')
parser.add_argument('player', type=lambda s: s.upper())
parser.add_argument('timeout', help='Timeout value in seconds ranging from 2 to 10000')
parser.add_argument('ip_address')

args = parser.parse_args()
turn = Player.get_turn(args.player)

# checks
if not 2 <= int(args.timeout) <= 10000:
    raise ValueError('Timeout ranges from 2 to 10000')

conn = ServerConnector(ip_address=args.ip_address, port=Player.port(turn))
conn.send_msg(conv.convert_team_name('SPTeam'))

if turn == Player.W:
    initial_state = conv.convert_state(conn.read())
else:
    conn.read()
    initial_state = conv.convert_state(conn.read())

print(initial_state)

while not initial_state.is_terminal(turn):
    root_node = Node(state=initial_state,
                     action_performed=None,
                     turn=turn,
                     parent_node=None,
                     depth=0)

    tree = Tree(root_node=root_node, ucb_constant=1)
    best_action, iter_n = tree.uct(timeout=int(args.timeout) - 1)

    print('iterations: %d\n' % iter_n)

    # send action
    conn.send_msg(conv.convert_action(best_action, turn=turn))
    # read state
    enemy_state = conv.convert_state(conn.read())

    print('%s turn:' % str(Player.next_turn(turn)))
    print(enemy_state)

    initial_state = conv.convert_state(conn.read())
    print('our turn with action %s:' % best_action)
    print(initial_state)
