
import agent.Network as Network
import numpy as np
import tensorflow as tf
import random
import collections

class Agent:

    def __init__(self, _inputList, _outputList):
        self.input_list = _inputList
        self.output_list = _outputList

    def InitNetwork(self):
        self.session = tf.Session()
        self.network = Network.Network(self.session, len(self.input_list), len(self.output_list), 'main')
        self.session.run(tf.global_variables_initializer())
        self.state = [0] * len(self.input_list)

    def Input(self, _data):
        self.state = [None] * len(self.input_list)
        for i in range(len(self.input_list)):
            self.state[i] = _data[self.input_list[i]]
        label = self.network.Decide(self.state)
        self.network.Train([self.state], label)

    def Output(self):
        decision = self.network.Decide(self.state)
        return self.output_list[np.argmax(decision)]