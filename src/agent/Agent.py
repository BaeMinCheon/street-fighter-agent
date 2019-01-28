
import agent.Network as Network
import random

class Agent:

    def __init__(self):
        print('Agent.__init__()')
        self.network = Network.Network()

    def Input(self, _list):
        pass

    def Output(self):
        action = []
        action.append(random.randrange(0, 5))
        action.append(random.randrange(0, 5))
        return action