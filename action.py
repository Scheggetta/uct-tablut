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
        return 'from: %s to: %s' % (self.frm, self.to)
