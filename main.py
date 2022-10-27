from server_connector import ServerConnector
import converter as conv
from action import Action

conn = ServerConnector(ip_address='localhost', port=5800)

conn_enemy = ServerConnector(ip_address='localhost', port=5801)

name = conv.convert_team_name('SPTeam')
name_enemy = conv.convert_team_name('Pippe')

conn.send_msg(name)
# conn.read()
conn_enemy.send_msg(name_enemy)
# conn_enemy.read()

conn.read()
conn_enemy.read()

msg = conv.convert_action(Action(frm=(3, 5), to=(3, 6)), turn='WHITE')
conn.send_msg(msg)

conn.read()
conn_enemy.read()

msg = conv.convert_action(Action(frm=(6, 1), to=(7, 1)), turn='BLACK')
conn_enemy.send_msg(msg)

conn.read()
conn_enemy.read()
