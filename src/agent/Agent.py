
import agent.Network as Network
import numpy as np
import tensorflow as tf
import random
import collections

class Agent:

    def __init__(self, _inputSize, _outputSize, _discount):
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())

    def Input(self, _data):
        pass

    def Output(self):
        return random.randrange(0, 25)