import numpy as np

import Server
import Agent


def GetStack(_main, _target, _batch):
    stackX = np.empty(0).reshape(0, _main.input_size)
    stackY = np.empty(0).reshape(0, _main.output_size)
    for currState, action, reward, nextState, isDone in _batch:
        Q = _main.Predict(currState)
        if isDone:
            Q[0, action] = reward
        else:
            Q[0, action] = reward + _main.discount * _target.Predict(nextState)[0, np.argmax(_main.Predict(nextState))]
        stackX = np.vstack([stackX, currState])
        stackY = np.vstack([stackY, Q])
    return stackX, stackY

def main():
    a = Agent.Agent(_inputSize=4, _outputSize=25, _discount=0.9)
    s = Server.Server('127.0.0.1', 7000)
    a.SetServer(s)
    a.Run()

if __name__ == '__main__':
    main()