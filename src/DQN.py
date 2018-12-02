import numpy as np
import tensorflow as tf


class DQN:

    def __init__(self, _session, _inputSize, _outputSize, _discount, _netName):
        self.session = _session
        self.input_size = _inputSize
        self.output_size = _outputSize
        self.discount = _discount
        self.network_name = _netName

    def InitNet(self, _hiddenSize = 100, _learnRate = 0.01):
        with tf.variable_scope(self.network_name):
            self.input = tf.placeholder(tf.float32, [None, self.input_size], name='INPUT')

            weight01 = tf.get_variable(name='WEIGHT_01', shape=[self.input_size, _hiddenSize], initializer=tf.contrib.layers.xavier_initializer())
            output01 = tf.nn.tanh(tf.matmul(self.input, weight01))

            weight02 = tf.get_variable(name='WEIGHT_02', shape=[_hiddenSize, self.output_size], initializer=tf.contrib.layers.xavier_initializer())
            output02 = tf.matmul(output01, weight02)

            self.output = output02

        self.label = tf.placeholder(shape=[None, self.output_size], dtype=tf.float32)
        self.error = tf.reduce_mean(tf.square(tf.subtract(self.label, self.output)))
        self.train = tf.train.AdamOptimizer(learning_rate=_learnRate).minimize(self.error)

    def Train(self, _x, _y):
        return self.session.run([self.error, self.train], feed_dict={self.input: _x, self.label: _y})

    def Predict(self, _state):
        reshapedState = np.reshape(_state, [1, self.input_size])
        return self.session.run(self.output, feed_dict={self.input: reshapedState})

    @staticmethod
    def GetSyncWeights(_srcNet = 'main', _dstNet = 'target'):
        srcVarList = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=_srcNet)
        dstVarList = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=_dstNet)

        opList = []
        for srcVar, dstVar in zip(srcVarList, dstVarList):
            opList.append(dstVar.assign(srcVar.value()))

        return opList