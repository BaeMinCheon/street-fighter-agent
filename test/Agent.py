import random


class Agent:

    def __init__(self):
        pass

    def Train(self, _list):
        pass

    def Action(self):
        action = []
        action.append(random.randrange(0, 5))
        action.append(random.randrange(0, 5))
        return action