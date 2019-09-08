
import manager.Server as Server
import agent.Agent as Agent
import os
import json

class Manager:

    def __init__(self):
        self.LoadConfig()
        self.server = Server.Server('127.0.0.1', 7000)
        self.agent = Agent.Agent(4, len(self.keymap), 0.9)
        self.widget = None
        self.is_running = False
        self.count_frame = 0
        self.control_code = ''

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
                    action = self.PostProcess(decision)
                    self.server.Send(action)
                else:
                    action = self.PostProcess(control)
                    self.server.Send(action)
            else:
                break

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

    def PostProcess(self, _output):
        if type(_output) is list:
            return _output
        else:
            return self.keymap[_output]

    def LoadConfig(self):
        manager_directory = os.path.dirname(os.path.realpath(__file__))
        script_directory = os.path.join(manager_directory, 'scripts')
        preprocess_path = os.path.join(script_directory, 'preprocess.code')
        keymap_path = os.path.join(script_directory, 'keymap.json')
        self.preprocess_code = open(preprocess_path, 'r').read()
        keymap_string = open(keymap_path, 'r').read()
        self.keymap = json.loads(keymap_string)['keymap']