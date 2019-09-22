
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
        self.prev_feature = {}

    def InitAgent(self):
        self.agent = Agent.Agent(self.agent_config)
        for key in self.agent_config['prev_list']:
            self.prev_feature[key] = 0

    def LoadModel(self, _filepath):
        self.agent.LoadModel(_filepath)

    def SaveModel(self, _filepath):
        self.agent.SaveModel(_filepath)

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
        try:
            self.is_running = True
            self.server.InitSocket()
            self.server.Accept()
            self.Run()
        except:
            pass
        finally:
            self.widget.server.OnClickStopServer()

    def Stop(self):
        print()
        print('Manager.Stop()')
        self.is_running = False
        self.server.Close()

    def PreProcess(self, _input):
        feature = {}
        if len(_input) > 0:
            locals = {'prev': self.prev_feature, 'data': _input, 'feature': feature}
            exec(self.preprocess_code, {}, locals)
            for key in self.prev_feature:
                feature[key + '.Diff'] = feature[key] - self.prev_feature[key]
                self.prev_feature[key] = feature[key]
        return feature

    def NeedAgent(self, _feature):
        control = []
        locals = {'self': self, 'feature': _feature, 'control': control}
        exec(self.control_code, {}, locals)
        need_agent = True
        if len(locals['control']) == 3:
            need_agent = False
        return need_agent, locals['control']