
import Agent

class Manager:

    def __init__(self):
        print('Manager.__init__()')
        self.agent = Agent.Agent()

    def Run(self):
        print('Manager.Run()')
        self.agent.Run()