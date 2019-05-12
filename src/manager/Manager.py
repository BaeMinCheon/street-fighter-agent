
import threading
import manager.Server as Server
import agent.Agent as Agent

Thread = threading.Thread

class Manager:

    def __init__(self):
        self.server = Server.Server('127.0.0.1', 7000)
        self.agent = Agent.Agent(4, 25, 0.9)
        self.widget = None
        self.is_running = False
        self.count_frame = 0
        self.control_code = ""

    def Run(self):
        self.count_frame = 0
        self.server.Send(0, 0)
        while self.is_running:
            self.count_frame += 1
            if self.server.Receive():
                self.server.PrintData()
                control = self.ControlGame(self.server.GetData())
                if len(control) > 0:
                    self.server.Send(control[0], control[1], control[2])
                else:
                    self.agent.Input(self.server.GetData())
                    output = self.agent.Output()
                    self.server.Send(output[0], output[1])
            else:
                break

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
        self.Run()

    def Stop(self):
        print()
        print('Manager.Stop()')
        self.is_running = False
        self.server.Close()

    def UpdateCode(self):
        self.control_code = self.widget.tb1.text

    def ControlGame(self, _data):
        control = []
        locals = {'self': self, '_data': _data, 'control': control}
        exec(self.control_code, {}, locals)
        return locals['control']