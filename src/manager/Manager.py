
import manager.Server as Server
import agent.Agent as Agent

class Manager:

    def __init__(self):
        self.server = Server.Server('127.0.0.1', 7000)
        self.agent = Agent.Agent(4, 25, 0.9)

    def Run(self):
        while True:
            self.server.Accept()
            while True:
                self.server.Send(self.agent.Output())
                if self.server.Receive():
                    self.agent.Input(self.server.GetList())
                else:
                    break