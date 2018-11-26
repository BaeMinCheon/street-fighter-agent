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

        self.step_number = 0;
        self.replay_buffer = collections.deque()

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

    def Action(self, _isRandom, _list = None):
        if _isRandom:
            action = []
            action.append(random.randrange(0, 5))
            action.append(random.randrange(0, 5))
        else:
            action = np.argmax(self.main.Predict(_list))
        return action