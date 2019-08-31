
import numpy as np
import tensorflow as tf

class Network:

    def __init__(self, _session, _inputSize, _outputSize, _discount, _netName):
        self.session = _session
        self.size_input = _inputSize
        self.size_output = _outputSize
        self.discount = _discount
        self.network_name = _netName
        self.InitNet(100, 0.01)

    def InitNet(self, _hiddenSize, _learnRate):
        with tf.variable_scope(self.network_name):
            self.input = tf.placeholder(tf.float32, shape=[None, self.size_input], name='input')

            weight01 = tf.get_variable(name='weight_01', shape=[self.size_input, _hiddenSize], initializer=tf.contrib.layers.xavier_initializer())
            output01 = tf.nn.tanh(tf.matmul(self.input, weight01))

            weight02 = tf.get_variable(name='weight_02', shape=[_hiddenSize, self.size_output], initializer=tf.contrib.layers.xavier_initializer())
            output02 = tf.matmul(output01, weight02)

            self.output = output02

        self.label = tf.placeholder(shape=[None, self.size_output], dtype=tf.float32)
        self.error = tf.reduce_mean(tf.square(tf.subtract(self.label, self.output)))
        self.train = tf.train.AdamOptimizer(learning_rate=_learnRate).minimize(self.error)

    def Train(self, _input, _label):
        return self.session.run([self.error, self.train], feed_dict={self.input: _input, self.label: _label})

    def Decide(self, _state):
        reshapedState = np.reshape(_state, [1, self.size_input])
        return self.session.run(self.output, feed_dict={self.input: reshapedState})