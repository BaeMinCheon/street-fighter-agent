
import agent.Network as Network
import numpy as np
import tensorflow as tf
import random
import collections

class Agent:

    def __init__(self, _inputSize, _outputSize, _discount):
        self.session = tf.Session()
        self.network = Network.Network(self.session, _inputSize, _outputSize, _discount, 'main')
        self.session.run(tf.global_variables_initializer())
        self.state = [0] * _inputSize

    def Input(self, _data):
        self.state = [_data['P1.IsLeft'], _data['Gap.X'], _data['Gap.Y'], _data['P1.CanAction']]
        label = self.network.Decide(self.state)
        self.network.Train([self.state], label)

    def Output(self):
        decision = self.network.Decide(self.state)
        return np.argmax(decision)