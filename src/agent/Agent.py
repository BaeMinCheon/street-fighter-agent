
import agent.Model as Model
import numpy as np
import tensorflow as tf
import random
import collections

def GetStacks(_main, _target, _batch):
    stack_x = np.empty(0).reshape(0, _main.size_input)
    stack_y = np.empty(0).reshape(0, _main.size_output)
    for curr_state, decision, reward, next_state in _batch:
        curr_main_Q = _main.Decide(curr_state)
        next_main_Q = _main.Decide(next_state)
        next_target_Q = _target.Decide(next_state)
        curr_main_Q[0][decision] = float(reward) + _main.discount * next_target_Q[0][np.argmax(next_main_Q)]
    stack_x = np.vstack([stack_x, curr_state])
    stack_y = np.vstack([stack_y, curr_main_Q])
    return stack_x, stack_y

class Agent:

    def __init__(self, _agentConfig):
        self.input_list = _agentConfig['input_list']
        self.output_list = _agentConfig['output_list']
        
        self.max_replay_number = _agentConfig['dqn']['max_replay_number']
        self.train_period = _agentConfig['dqn']['train_period']
        self.train_number = _agentConfig['dqn']['train_number']
        self.batch_size = _agentConfig['dqn']['batch_size']

        self.hidden_layer_size = _agentConfig['model']['hidden_layer_size']
        self.learning_rate = _agentConfig['model']['learning_rate']
        self.discount_rate = _agentConfig['model']['discount_rate']
        
        self.InitModel()

    def InitModel(self):
        tf.reset_default_graph()
        self.session = tf.Session()
        self.model_main = Model.Model('main', self)
        self.model_target = Model.Model('target', self)
        self.session.run(tf.global_variables_initializer())
        self.sync_op = Model.GetSyncOps('main', 'target')
        self.session.run(self.sync_op)

        self.state = [0] * len(self.input_list)
        self.decision = 0
        self.reward = 0
        self.number_decide = 0
        self.replay_queue = collections.deque()
        self.number_epoch = 0

    def LoadModel(self, _filepath):
        saver = tf.train.Saver()
        saver.restore(self.session, _filepath)

    def SaveModel(self, _filepath):
        saver = tf.train.Saver()
        saver.save(self.session, _filepath)

    def Input(self, _feature):
        self.reward = _feature['Reward']
        next_state = [None] * len(self.input_list)
        for i in range(len(self.input_list)):
            self.state[i] = _feature[self.input_list[i]]
        self.replay_queue.append((self.state, self.decision, self.reward, next_state))
        if len(self.replay_queue) > self.max_replay_number:
            self.replay_queue.popleft()
        self.state = next_state

        if (self.number_decide % self.train_period) == (self.train_period - 1):
            for i in range(self.train_number):
                batch = random.sample(self.replay_queue, self.batch_size)
                stack_x, stack_y = GetStacks(self.model_main, self.model_target, batch)
                self.model_main.Train(stack_x, stack_y)
            self.number_epoch += self.train_number
            self.session.run(self.sync_op)

    def Output(self):
        self.number_decide += 1
        random_boundary = 1.0 / float(1 + self.number_decide / self.train_period)
        if np.random.rand(1) < random_boundary:
            self.decision = random.randrange(0, len(self.output_list))
        else:
            self.decision = np.argmax(self.model_main.Decide(self.state))
        return self.output_list[self.decision]