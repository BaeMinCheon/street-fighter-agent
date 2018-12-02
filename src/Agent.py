import random
import numpy as np
import tensorflow as tf
import collections
import DQN
import Server

class Agent:

    def __init__(self, _inputSize, _outputSize, _discount):
        self.session = tf.Session()
        self.main = DQN.DQN(self.session, _inputSize, _outputSize, _discount, 'main')
        self.main.InitNet()
        self.target = DQN.DQN(self.session, _inputSize, _outputSize, _discount, 'target')
        self.target.InitNet()
        self.session.run(tf.global_variables_initializer())

        self.syncOps = self.main.GetSyncWeights('main', 'target')
        self.session.run(self.syncOps)

        self.step_number = 0
        self.replay_buffer = collections.deque()

        self.key_map = { 0:[0, 0], 1:[0, 1], 2:[0, 2], 3:[0, 3], 4:[0, 4],
        5:[1, 0], 6:[1, 1], 7:[1, 2], 8:[1, 3], 9:[1, 4],
        10:[2, 0], 11:[2, 1], 12:[2, 2], 13:[2, 3], 14:[2, 4],
        15:[3, 0], 16:[3, 1], 17:[3, 2], 18:[3, 3], 19:[3, 4],
        20:[4, 0], 21:[4, 1], 22:[4, 2], 23:[4, 3], 24:[4, 4] }

    def SetServer(self, _server):
        self.server = _server

    def Run(self):
        while True:
            self.server.Accept()

            while True:
                if self.server.Receive():
                    #self.server.Print()
                    self.server.Send(self.Train(self.server.GetFeatures()))
                else:
                    break

    def Train(self, _list):
        listFloat = [float(_list[0]), float(_list[1]), float(_list[2]), float(_list[4])]
        self.step_number = self.step_number + 1
        randomBoundary = 1.0 / (self.step_number / 10 + 1)
        if np.random.rand(1) < randomBoundary:
            retVal = self.Action(True)
        else:
            retVal = self.Action(False, listFloat)

        self.replay_buffer.append(listFloat)
        if len(self.replay_buffer) > 50000:
            self.replay_buffer.popleft()

        return retVal

    def Action(self, _isRandom, _list = None):
        if _isRandom:
            action = []
            action.append(random.randrange(0, 5))
            action.append(random.randrange(0, 5))
        else:
            action = self.key_map[np.argmax(self.main.Predict(_list).flatten())]
        return action