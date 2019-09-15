
import numpy as np
import tensorflow as tf

def GetSyncOps(_srcName, _dstName):
    src_var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=_srcName)
    dst_var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=_dstName)
    op_list = []
    for src_var, dst_var in zip(src_var_list, dst_var_list):
        op_list.append(dst_var.assign(src_var.value()))
    return op_list

class Model:

    def __init__(self, _netName, _agent):
        self.model_name = _netName
        self.session = _agent.session
        self.size_input = len(_agent.input_list)
        self.size_output = len(_agent.output_list)
        self.discount = _agent.discount_rate
        
        self.InitNet(_agent.hidden_layer_size, _agent.learning_rate)

    def InitNet(self, _hiddenSize, _learnRate):
        with tf.variable_scope(self.model_name):
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