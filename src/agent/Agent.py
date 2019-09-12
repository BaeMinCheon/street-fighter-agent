
import agent.Model as Model
import numpy as np
import tensorflow as tf
import random
import collections

class Agent:

    def __init__(self, _inputList, _outputList):
        self.input_list = _inputList
        self.output_list = _outputList

    def InitModel(self):
        tf.reset_default_graph()
        self.session = tf.Session()
        self.mdoel = Model.Model(self.session, len(self.input_list), len(self.output_list), 'main')
        self.session.run(tf.global_variables_initializer())
        self.state = [0] * len(self.input_list)

    def LoadModel(self, _filepath):
        saver = tf.train.Saver()
        saver.restore(self.session, _filepath)

    def SaveModel(self, _filepath):
        saver = tf.train.Saver()
        saver.save(self.session, _filepath)

    def Input(self, _data):
        self.state = [None] * len(self.input_list)
        for i in range(len(self.input_list)):
            self.state[i] = _data[self.input_list[i]]
        label = self.Model.Decide(self.state)
        self.Model.Train([self.state], label)

    def Output(self):
        decision = self.Model.Decide(self.state)
        return self.output_list[np.argmax(decision)]