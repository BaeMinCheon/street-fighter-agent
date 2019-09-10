
import manager.Server as Server
import agent.Agent as Agent

class Manager:

    def __init__(self):
        self.server = Server.Server('127.0.0.1', 7000)
        self.agent = None
        self.widget = None
        self.is_running = False
        self.count_frame = 0
        self.preprocess_code = ''
        self.control_code = ''
        self.agent_config = {}

    def InitAgent(self):
        self.agent = Agent.Agent(self.agent_config['input_list'], self.agent_config['output_list'])
        self.agent.InitNetwork()

    def LoadNetwork(self, _filepath):
        self.agent.LoadNetwork(_filepath)

    def SaveNetwork(self, _filepath):
        self.agent.SaveNetwork(_filepath)

    def Run(self):
        self.count_frame = 0
        self.server.Send()
        while self.is_running:
            self.count_frame += 1
            if self.server.Receive():
                self.server.PrintData()
                feature = self.PreProcess(self.server.data)
                need_agent, control = self.NeedAgent(feature)
                if need_agent:
                    self.agent.Input(feature)
                    decision = self.agent.Output()
                    self.server.Send(decision)

                    self.widget.server.label_train_check.text = 'Agent Status : Train On'
                else:
                    self.server.Send(control)

                    self.widget.server.label_train_check.text = 'Agent Status : Train Off'
            else:
                break

    def Start(self):
        print()
        print('Manager.Start()')
        self.is_running = True
        self.server.InitSocket()
        self.server.Accept()
        self.Run()

    def Stop(self):
        print()
        print('Manager.Stop()')
        self.is_running = False
        self.server.Close()

    def PreProcess(self, _input):
        feature = {}
        locals = {'self': self, 'data': _input, 'feature': feature}
        exec(self.preprocess_code, {}, locals)
        return feature

    def NeedAgent(self, _feature):
        control = []
        locals = {'self': self, 'feature': _feature, 'control': control}
        exec(self.control_code, {}, locals)
        need_agent = True
        if len(locals['control']) == 3:
            need_agent = False
        return need_agent, locals['control']