
import agent.Network as Network
import numpy as np
import tensorflow as tf
import random

key_map = { 0:[0, 0], 1:[0, 1], 2:[0, 2], 3:[0, 3], 4:[0, 4],
        5:[1, 0], 6:[1, 1], 7:[1, 2], 8:[1, 3], 9:[1, 4],
        10:[2, 0], 11:[2, 1], 12:[2, 2], 13:[2, 3], 14:[2, 4],
        15:[3, 0], 16:[3, 1], 17:[3, 2], 18:[3, 3], 19:[3, 4],
        20:[4, 0], 21:[4, 1], 22:[4, 2], 23:[4, 3], 24:[4, 4] }

class Agent:

    def __init__(self, _inputSize, _outputSize, _discount):
        self.session = tf.Session()
        self.network_main = Network.Network(self.session, _inputSize, _outputSize, _discount, 'main')
        self.network_target = Network.Network(self.session, _inputSize, _outputSize, _discount, 'target')
        self.session.run(tf.global_variables_initializer())
        self.sync_operation = Network.GetSyncWeights('main', 'target')
        self.session.run(self.sync_operation)

        self.action = 0
        self.number_train = 0

    def Input(self, _list):
        random_boundary = 1.0 / float(1 + self.number_train / 10)
        if np.random.rand(1) < random_boundary:
            rand = random.randrange(0, 25)
            self.action = key_map[rand]
        else:
            predict = self.network_main.Predict(_list)
            self.action = key_map[np.argmax(predict)]
        self.number_train += 1

    def Output(self):
        return self.action