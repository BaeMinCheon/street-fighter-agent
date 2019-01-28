
import Network

class Agent:

    def __init__(self):
        print('Agent.__init__()')
        self.network = Network.Network()

    def Run(self):
        print('Agent.Run()')
        self.network.Run()