
import manager.Server as Server
import agent.Agent as Agent

class Manager:

    def __init__(self):
        print('Manager.__init__()')
        self.server = Server.Server('127.0.0.1', 7000)
        self.agent = Agent.Agent()

    def Run(self):
        while True:
            self.server.Accept()
            while True:
                if self.server.Receive():
                    self.agent.Input(self.server.GetList())
                    self.server.Send(self.agent.Output())
                else:
                    break