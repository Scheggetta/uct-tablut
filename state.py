class State:
    def __init__(self, whites, blacks, king):
        self.__s = [whites, blacks, king]

    @property
    def s(self):
        return self.__s

    @property
    def whites(self):
        return self.s[0]

    @property
    def blacks(self):
        return self.s[1]

    @property
    def king(self):
        return self.s[2]

    @king.setter
    def king(self, value):
        self.s[2] = value
