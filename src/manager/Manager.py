
import threading
import manager.Server as Server
import agent.Agent as Agent

Thread = threading.Thread

class Manager:

    def __init__(self):
        self.server = Server.Server('127.0.0.1', 7000)
        self.agent = Agent.Agent(4, 25, 0.9)
        self.is_running = False

    def Loop(self):
        while self.is_running:
            self.server.Send(self.agent.Output())
            if self.server.Receive():
                self.agent.Input(self.server.GetData())
            else:
                break
            #self.server.PrintData()

    def OnClickStart(self):
        t = Thread(target=self.Start)
        t.daemon = True
        t.start()

    def OnClickStop(self):
        t = Thread(target=self.Stop)
        t.daemon = True
        t.start()

    def Start(self):
        print()
        print('Manager.Start()')
        self.is_running = True
        self.server.Accept()
        self.Loop()

    def Stop(self):
        print()
        print('Manager.Stop()')
        self.is_running = False
        self.server.Close()