
import agent.Network as Network
import numpy as np
import tensorflow as tf
import random
import collections

key_map = { 0:[0, 0], 1:[0, 1], 2:[0, 2], 3:[0, 3], 4:[0, 4],
        5:[1, 0], 6:[1, 1], 7:[1, 2], 8:[1, 3], 9:[1, 4],
        10:[2, 0], 11:[2, 1], 12:[2, 2], 13:[2, 3], 14:[2, 4],
        15:[3, 0], 16:[3, 1], 17:[3, 2], 18:[3, 3], 19:[3, 4],
        20:[4, 0], 21:[4, 1], 22:[4, 2], 23:[4, 3], 24:[4, 4] }

MAX_NUMBER_REPLAY = 50000

def GetStack(_main, _target, _batch):
    stackX = np.empty(0).reshape(0, _main.size_input)
    stackY = np.empty(0).reshape(0, _main.size_output)
    for stateCurr, action, reward, StateNext in _batch:
        Q = _main.Predict(stateCurr)
        Q_main_next = _main.Predict(StateNext)
        Q_target_next = _target.Predict(StateNext)
        Q[0][action] = float(reward) + _main.discount * Q_target_next[0][np.argmax(Q_main_next)]
    stackX = np.vstack([stackX, stateCurr])
    stackY = np.vstack([stackY, Q])
    return stackX, stackY

class Agent:

    def __init__(self, _inputSize, _outputSize, _discount):
        self.session = tf.Session()
        self.network_main = Network.Network(self.session, _inputSize, _outputSize, _discount, 'main')
        self.network_target = Network.Network(self.session, _inputSize, _outputSize, _discount, 'target')
        self.session.run(tf.global_variables_initializer())
        self.sync_operation = Network.GetSyncWeights('main', 'target')
        self.session.run(self.sync_operation)

        self.state = [0, 0, 0, 0]
        self.action = 0
        self.reward = 0
        self.number_action = 0
        self.deque_replay = collections.deque()

    def Input(self, _data):
        self.reward = _data['Gap.HP.P1']
        nextState = [_data['P1.IsLeft'], _data['Gap.X'], _data['Gap.Y'], _data['P1.CanAction']]
        self.deque_replay.append((self.state, self.action, self.reward, nextState))
        self.state = nextState
        if self.number_action % 1000 == 999:
            for i in range(50):
                batch = random.sample(self.deque_replay, 10)
                stackX, stackY = GetStack(self.network_main, self.network_target, batch)
                self.network_main.Train(stackX, stackY)
            self.session.run(self.sync_operation)
            print("action number : {}".format(self.number_action))

    def Output(self):
        random_boundary = 1.0 / float(1 + self.number_action / 10)
        if np.random.rand(1) < random_boundary:
            rand = random.randrange(0, 25)
            self.action = rand
        else:
            predict = self.network_main.Predict(self.state)
            self.action = np.argmax(predict)
        self.number_action += 1
        return key_map[self.action]