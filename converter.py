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


def from_string_to_board(string_to_convert: str) -> list:
    js: dict = json.loads(string_to_convert)
    board = js['board']
    return board


def from_board_to_state(board: list) -> State:
    # TODO: check SetList conversion
    fnc = lambda checker: [(j + 1, i + 1) for i, line in enumerate(board) for j, elm in enumerate(line) if elm == checker]
    whites = fnc('WHITE')
    blacks = fnc('BLACK')
    # TODO: test case if the terminal state has no king
    king = fnc('KING')[0]

    return State(whites, blacks, king)


def convert_state(data_in_bytes: bytes) -> State:
    return from_board_to_state(from_string_to_board(from_byte_to_string(data_in_bytes)))
