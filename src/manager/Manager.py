
import os
import sys
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent'))
sys.path.append(lib_path)

import Agent

class Manager:

    def __init__(self):
        print('Manager.__init__()')
        self.agent = Agent.Agent()

    def Run(self):
        print('Manager.Run()')
        self.agent.Run()