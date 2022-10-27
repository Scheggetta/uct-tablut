import string
import json

from state import State
from action import Action


from_int_to_str = {i: v for i, v in zip(range(1, 10), string.ascii_lowercase[:10])}


# methods to encode actions
def from_action_to_string(a: Action, turn: str) -> str:
    frm = from_int_to_str[a.frm[0]] + str(a.frm[1])
    to = from_int_to_str[a.to[0]] + str(a.to[1])
    js = {
        'from': frm,
        'to': to,
        'turn': turn
    }
    return json.dumps(js)


def from_string_to_bytes(_str: str) -> bytes:
    bytes_str = _str.encode()
    return len(bytes_str).to_bytes(4, byteorder='big') + bytes_str


def convert_action(a: Action, turn) -> bytes:
    return from_string_to_bytes(from_action_to_string(a, turn))


def convert_team_name(team_name: str):
    return from_string_to_bytes(team_name)


# methods to decode states
def from_byte_to_string(data: bytes) -> str:
    size = int.from_bytes(data[:4], byteorder='big')
    buf = data[4: 4 + size]
    return buf.decode()


def from_string_to_json(string_to_convert: str) -> json:
    js = json.loads(string_to_convert)
    board = js['board']


def from_json_to_state(json_to_convert: json) -> State:
    pass
