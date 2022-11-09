import copy

from state import State
from action import Action
from players import Players


class Env:
    castle = (5, 5)
    king_surroundings = [(5, 4), (6, 5), (5, 6), (4, 5)]

    north_camp = [(4, 1), (5, 1), (5, 2), (6, 1)]  # idx: 0
    east_camp = [(9, 4), (9, 5), (8, 5), (9, 6)]   # idx: 1
    south_camp = [(4, 9), (5, 9), (5, 8), (6, 9)]  # idx: 2
    west_camp = [(1, 4), (1, 5), (2, 5), (1, 6)]   # idx: 3

    camps = north_camp + east_camp + south_camp + west_camp

    # IMPORTANT: We assume that the list order in these variables will not be changed;
    # otherwise, unexpected behaviour will occur
    other_camps = [east_camp + south_camp + west_camp,
                   north_camp + south_camp + west_camp,
                   north_camp + east_camp + west_camp,
                   north_camp + east_camp + south_camp]

    @staticmethod
    def get_camp_position(checker):
        camps = [Env.north_camp, Env.east_camp, Env.south_camp, Env.west_camp]
        for idx, camp in enumerate(camps):
            if checker in camp:
                return idx

    def __init__(self):
        pass

    @staticmethod
    def get_available_moves(s: State, turn: Players) -> list[Action]:
        checkers = s.checkers(turn)

        recompute_other_checkers = False
        checkers_camp_position = {}
        if turn == Players.B:
            for checker in checkers:
                camp_position = Env.get_camp_position(checker)
                if camp_position is not None:
                    checkers_camp_position[checker] = camp_position
                    if not recompute_other_checkers:
                        recompute_other_checkers = True

        other_checkers_base = s.whites + s.blacks + [s.king, Env.castle]
        other_checkers = other_checkers_base + Env.camps

        moves = []

        for ch_col, ch_row in checkers:
            left = 0
            right = 10
            up = 0
            down = 10

            if recompute_other_checkers and (ch_col, ch_row) in checkers_camp_position:
                _other_checkers = other_checkers_base + Env.other_camps[checkers_camp_position[(ch_col, ch_row)]]
            else:
                _other_checkers = other_checkers

            for other_col, other_row in _other_checkers:
                if ch_col == other_col and ch_row == other_row:
                    continue
                elif ch_col == other_col:
                    if ch_row - other_row > 0:
                        # up
                        if other_row > up:
                            up = other_row
                    else:
                        # down
                        if other_row < down:
                            down = other_row
                elif ch_row == other_row:
                    if ch_col - other_col > 0:
                        # left
                        if other_col > left:
                            left = other_col
                    else:
                        # right
                        if other_col < right:
                            right = other_col

            moves += [Action((ch_col, ch_row), (ch_col, x)) for x in range(up + 1, down) if x != ch_row]
            moves += [Action((ch_col, ch_row), (y, ch_row)) for y in range(left + 1, right) if y != ch_col]

        return moves

    @staticmethod
    def transition_function(s: State, a: Action, turn: Players) -> State:
        next_s = copy.deepcopy(s)

        if turn == Players.W:
            if a.frm == s.king:
                next_s.king = a.to
            else:
                next_s.whites.replace(a.frm, a.to)
        else:
            next_s.blacks.replace(a.frm, a.to)

        adjacent_cells = Env.get_adjacent_cells(a)

        checkers_to_take = Env.checkers_to_take(next_s, a.to, adjacent_cells, turn)

        for checker in checkers_to_take:
            if turn == Players.B:
                if checker == next_s.king:
                    # TODO: set `next_s.king` to None
                    next_s.king = (0, 0)
                else:
                    next_s.whites.remove(checker)
            else:
                next_s.blacks.remove(checker)

        return next_s

    @staticmethod
    def checkers_to_take(s: State, current_checker: tuple, adjacent_cells: list[tuple], turn: Players) -> list[tuple]:
        ally_checkers = s.whites + [s.king] if turn == Players.W else s.blacks
        opponent_checkers = s.whites + [s.king] if turn == Players.B else s.blacks

        # sw_cell = sandwichable_cell
        sw_cells = [cell for cell in adjacent_cells if cell in opponent_checkers]

        res = []
        for swc in sw_cells:
            direction = 1 if current_checker[0] == swc[0] else 0
            heading = -1 if current_checker[direction] - swc[direction] > 0 else 1

            opposite_checker = (swc[0] + (1 - direction) * heading, swc[1] + direction * heading)

            if opposite_checker in Env.camps + [Env.castle] or opposite_checker in ally_checkers:
                if turn == Players.B and swc == s.king:
                    if swc == Env.castle:
                        # check if king is surrounded by four black checkers
                        if (opposite_checker[1], opposite_checker[0]) in s.blacks and \
                                (current_checker[1], current_checker[0]) in s.blacks:
                            res.append(swc)

                    elif swc in Env.king_surroundings:
                        # TODO: refactor
                        # check if king is surrounded by three black checkers
                        if current_checker[0] == Env.castle[0]:
                            # red
                            if (swc[0] - 1, swc[1]) in s.blacks and (swc[0] + 1, swc[1]) in s.blacks:
                                res.append(swc)
                        elif current_checker[1] == Env.castle[1]:
                            # red
                            if (swc[0], swc[1] - 1) in s.blacks and (swc[0], swc[1] + 1) in s.blacks:
                                res.append(swc)
                        else:
                            # green
                            if current_checker[0] == swc[0]:
                                if ((swc[0] - 1, swc[1]) in s.blacks or (swc[0] - 1, swc[1]) == Env.castle) and \
                                        ((swc[0] + 1, swc[1]) in s.blacks or (swc[0] + 1, swc[1]) == Env.castle):
                                    res.append(swc)
                            else:
                                if ((swc[0], swc[1] - 1) in s.blacks or (swc[0], swc[1] - 1) == Env.castle) and \
                                        ((swc[0], swc[1] + 1) in s.blacks or (swc[0], swc[1] + 1) == Env.castle):
                                    res.append(swc)
                    else:
                        res.append(swc)
                else:
                    res.append(swc)

        return res

    @staticmethod
    def get_adjacent_cells(a: Action) -> list[tuple]:
        # `direction` = 1 if the action moves the checker in the same column; 0 in the same row
        # `heading` = -1 if the action moves the checker towards a lower value on the same axis; otherwise, 1
        direction = 1 if a.frm[0] == a.to[0] else 0
        heading = -1 if a.frm[direction] - a.to[direction] > 0 else 1

        ch_col, ch_row = a.to
        res = []

        if direction == 1:
            if ch_col > 1:
                res.append((ch_col - 1, ch_row))
            if ch_col < 9:
                res.append((ch_col + 1, ch_row))
            if heading == -1:
                if ch_row > 1:
                    res.append((ch_col, ch_row - 1))
            else:
                if ch_row < 9:
                    res.append((ch_col, ch_row + 1))
        else:
            if ch_row > 1:
                res.append((ch_col, ch_row - 1))
            if ch_row < 9:
                res.append((ch_col, ch_row + 1))
            if heading == -1:
                if ch_col > 1:
                    res.append((ch_col - 1, ch_row))
            else:
                if ch_col < 9:
                    res.append((ch_col + 1, ch_row))

        return res
