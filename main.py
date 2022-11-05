from players import Players
from server_connector import ServerConnector
import converter as conv
from action import Action
from env import Env
from state import State
from setlist import SetList


'''s = State(SetList([(3, 3), (5, 4),
                   (6, 5), (7, 5),
                   (5, 6), (5, 7),
                   (3, 5), (4, 5)]),
          SetList([(4, 1), (5, 1), (5, 2), (6, 1),
                   (9, 4), (9, 5), (8, 5), (9, 6),
                   (4, 9), (5, 9), (5, 8), (6, 9),
                   (1, 4), (1, 5), (2, 5), (1, 9)]),
          (5, 5))

print(s)
print(Env.get_available_moves(s, Players.W))

for i in Env.get_available_moves(s, Players.W):
    print(i)
quit()'''
'''
def print_state(state: str):
    mappings = {'EMPTY': '0', 'WHITE': 'W', 'BLACK': 'B', 'KING': 'K'}
    res = ''
    for line in state:
        for checker in line:
            res += mappings[checker]
        res += '\n'
    return res

with open('js.pickle', 'wb') as f:
    pickle.dump(js, f)

with open('state.pickle', 'rb') as f:
    board = pickle.load(f)
'''

initial_state = State(SetList([(5, 3), (7, 5), (9, 3), (7, 1), (8, 1),
                               (2, 4), (2, 7), (4, 6)]),
                      SetList([(4, 3), (5, 2),
                               (7, 4), (7, 2), (8, 2),
                               (4, 7), (5, 8), (8, 4),
                               (3, 4), (2, 5), (3, 6)]),
                      (5, 5))



# print(initial_state)
# s1 = Env.transition_function(initial_state, Action((2, 7), (2, 6)), Players.W)
# print(s1)
#s2 = Env.transition_function(s1, Action((4, 7), (4, 6)), Players.B)
#print(s2)
#s3 = Env.transition_function(s2, Action((5, 8), (5, 7)), Players.B)
#print(s3)
#s4 = Env.transition_function(s3, Action((6, 7), (6, 6)), Players.B)
#print(s4)

conn = ServerConnector(ip_address='localhost', port=5800)

conn_enemy = ServerConnector(ip_address='localhost', port=5801)

name = conv.convert_team_name('SPTeam')
name_enemy = conv.convert_team_name('Enemy')

conn.send_msg(name)
conn_enemy.send_msg(name_enemy)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(5, 4), to=(2, 4)), turn='WHITE')
conn.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(1, 6), to=(1, 7)), turn='BLACK')
conn_enemy.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(5, 6), to=(2, 6)), turn='WHITE')
conn.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

'''msg = conv.convert_action(Action(frm=(6, 1), to=(9, 1)), turn='BLACK')
conn_enemy.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(5, 5), to=(4, 5)), turn='WHITE')
conn.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()'''



'''
The King gets captured by only one black checker if it is adjacent to a camp

msg = conv.convert_action(Action(frm=(6, 5), to=(6, 4)), turn='WHITE')
conn.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(9, 6), to=(7, 6)), turn='BLACK')
conn_enemy.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(7, 5), to=(7, 4)), turn='WHITE')
conn.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(7, 6), to=(6, 6)), turn='BLACK')
conn_enemy.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(5, 5), to=(7, 5)), turn='WHITE')
conn.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()

msg = conv.convert_action(Action(frm=(6, 6), to=(6, 5)), turn='BLACK')
conn_enemy.send_msg(msg)

print(conv.convert_state(conn.read()))
conn_enemy.read()
'''