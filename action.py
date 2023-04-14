import string

from_int_to_str = {i: v for i, v in zip(range(1, 10), string.ascii_uppercase[:10])}


class Action:
    def __init__(self, frm: tuple, to: tuple):
        self.__from = frm
        self.__to = to

    @property
    def frm(self) -> tuple:
        return self.__from

    @property
    def to(self) -> tuple:
        return self.__to

    def __str__(self):
        frm_letter = from_int_to_str[self.frm[0]]
        to_letter = from_int_to_str[self.to[0]]

        res = 'from: (%s, %d) -> to: (%s, %d)' % (frm_letter, self.frm[1], to_letter, self.to[1])
        return res
