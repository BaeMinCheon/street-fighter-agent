
import numpy as np
import tensorflow as tf

def GetSyncWeights(_srcNet = 'main', _dstNet = 'target'):
    srcVarList = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=_srcNet)
    dstVarList = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=_dstNet)

    opList = []
    for srcVar, dstVar in zip(srcVarList, dstVarList):
        opList.append(dstVar.assign(srcVar.value()))

    return opList

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
            self.input = tf.placeholder(tf.float32, [None, self.size_input], name='INPUT')

            weight01 = tf.get_variable(name='WEIGHT_01', shape=[self.size_input, _hiddenSize], initializer=tf.contrib.layers.xavier_initializer())
            output01 = tf.nn.tanh(tf.matmul(self.input, weight01))

            weight02 = tf.get_variable(name='WEIGHT_02', shape=[_hiddenSize, self.size_output], initializer=tf.contrib.layers.xavier_initializer())
            output02 = tf.matmul(output01, weight02)

            self.output = output02

        self.label = tf.placeholder(shape=[None, self.size_output], dtype=tf.float32)
        self.error = tf.reduce_mean(tf.square(tf.subtract(self.label, self.output)))
        self.train = tf.train.AdamOptimizer(learning_rate=_learnRate).minimize(self.error)

    def Train(self, _x, _y):
        pass

    def Predict(self, _state):
        pass