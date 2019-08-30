
import agent.Network as Network
import numpy as np
import tensorflow as tf
import random
import collections

MAX_NUMBER_REPLAY = 50000

def GetStack(_main, _target, _batch):
    stack_x = np.empty(0).reshape(0, _main.size_input)
    stack_y = np.empty(0).reshape(0, _main.size_output)
    for stateCurr, action, reward, StateNext in _batch:
        Q = _main.Predict(stateCurr)
        Q_main_next = _main.Predict(StateNext)
        Q_target_next = _target.Predict(StateNext)
        Q[0][action] = float(reward) + _main.discount * Q_target_next[0][np.argmax(Q_main_next)]
    stack_x = np.vstack([stack_x, stateCurr])
    stack_y = np.vstack([stack_y, Q])
    return stack_x, stack_y

class Agent:

    def __init__(self, _inputSize, _outputSize, _discount):
        self.session = tf.Session()
        self.network_main = Network.Network(self.session, _inputSize, _outputSize, _discount, 'main')
        self.network_target = Network.Network(self.session, _inputSize, _outputSize, _discount, 'target')
        self.session.run(tf.global_variables_initializer())
        self.sync_operation = Network.GetSyncWeights('main', 'target')
        self.session.run(self.sync_operation)

        self.state = [0, 0, 0, 0]
        self.decision = 0
        self.reward = 0
        self.number_action = 0
        self.deque_replay = collections.deque()

    def Input(self, _data):
        self.reward = _data['Gap.HP.P1']
        nextState = [_data['P1.IsLeft'], _data['Gap.X'], _data['Gap.Y'], _data['P1.CanAction']]
        self.deque_replay.append((self.state, self.decision, self.reward, nextState))
        self.state = nextState
        if self.number_action % 1000 == 999:
            for i in range(50):
                batch = random.sample(self.deque_replay, 10)
                stack_x, stack_y = GetStack(self.network_main, self.network_target, batch)
                self.network_main.Train(stack_x, stack_y)
            self.session.run(self.sync_operation)
            print("action number : {}".format(self.number_action))

    def Output(self):
        random_boundary = 1.0 / float(1 + self.number_action / 10)
        if np.random.rand(1) < random_boundary:
            rand = random.randrange(0, 25)
            self.decision = rand
        else:
            predict = self.network_main.Predict(self.state)
            self.decision = np.argmax(predict)
        self.number_action += 1
        return self.decision