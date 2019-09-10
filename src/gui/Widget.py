
import kivy.config
import kivy.app
import kivy.uix.label
import kivy.uix.button
import kivy.uix.boxlayout
import kivy.uix.gridlayout
import kivy.uix.floatlayout
import kivy.uix.textinput
import kivy.uix.popup
import kivy.properties
import kivy.factory
import os
import threading
import json

Config = kivy.config.Config
App = kivy.app.App
Label = kivy.uix.label.Label
Button = kivy.uix.button.Button
BoxLayout = kivy.uix.boxlayout.BoxLayout
GridLayout = kivy.uix.gridlayout.GridLayout
FloatLayout = kivy.uix.floatlayout.FloatLayout
TextInput = kivy.uix.textinput.TextInput
Popup = kivy.uix.popup.Popup
ObjectProperty = kivy.properties.ObjectProperty
Factory = kivy.factory.Factory
Config.set('input', 'mouse', 'mouse,disable_multitouch')

Thread = threading.Thread

class RootWidget(BoxLayout):

    def __init__(self, _manager):
        super(RootWidget, self).__init__()
        self.manager = _manager
        self.manager.widget = self
        self.server = None
        self.config = None

    def OnStart(self):
        self.server.button_start_server.disabled = True
        self.server.button_stop_server.disabled = False
        self.server.button_init_agent.disabled = True
        self.server.button_load_network.disabled = True
        self.server.button_save_network.disabled = True
        self.server.textinput_ip.disabled = True
        self.manager.server.ip_server = self.server.textinput_ip.text
        self.server.textinput_port.disabled = True
        self.manager.server.port_server = int(self.server.textinput_port.text)

        self.config.button_load_preprocess.disabled = True
        self.config.textinput_preprocess.disabled = True
        self.config.button_load_control.disabled = True
        self.config.textinput_control.disabled = True
        self.config.button_load_agent_config.disabled = True
        self.config.textinput_agent_config.disabled = True
        self.config.button_load_network.disabled = True
        self.config.textinput_network.disabled = True

        t = Thread(target=self.manager.Start)
        t.daemon = True
        t.start()

    def OnStop(self):
        self.server.button_start_server.disabled = False
        self.server.button_stop_server.disabled = True
        self.server.button_init_agent.disabled = False
        self.server.button_save_network.disabled = False
        self.server.textinput_ip.disabled = False
        self.server.textinput_port.disabled = False

        self.config.button_load_preprocess.disabled = False
        self.config.textinput_preprocess.disabled = False
        self.config.button_load_control.disabled = False
        self.config.textinput_control.disabled = False
        self.config.button_load_agent_config.disabled = False
        self.config.textinput_agent_config.disabled = False
        self.config.button_load_network.disabled = False
        self.config.textinput_network.disabled = False

        t = Thread(target=self.manager.Stop)
        t.daemon = True
        t.start()

class ServerWidget(BoxLayout):

    root = None

    button_start_server = ObjectProperty(None)
    button_stop_server = ObjectProperty(None)
    button_init_agent = ObjectProperty(None)
    button_load_network = ObjectProperty(None)
    button_save_network = ObjectProperty(None)
    textinput_ip = ObjectProperty(None)
    textinput_port = ObjectProperty(None)
    label_train_check = ObjectProperty(None)

    func_start = ObjectProperty(None)
    func_stop = ObjectProperty(None)

    def OnClickInitializeAgent(self):
        self.root.manager.InitAgent()
        self.button_start_server.disabled = False
        self.button_load_network.disabled = False
        self.button_save_network.disabled = False

    def OnClickLoadNetwork(self):
        self.root.manager.LoadNetwork()

    def OnClickSaveNetwork(self):
        self.root.manager.SaveNetwork()

class ConfigWidget(GridLayout):

    root = None

    button_load_preprocess = ObjectProperty(None)
    button_load_control = ObjectProperty(None)
    button_load_agent_config = ObjectProperty(None)
    button_load_network = ObjectProperty(None)
    textinput_preprocess = ObjectProperty(None)
    textinput_control = ObjectProperty(None)
    textinput_agent_config = ObjectProperty(None)
    textinput_network = ObjectProperty(None)

    def ShowLoadDialog(self, _textinput, _onSuccess = None):
        content = LoadDialog(func_load=self.Load, func_cancel=self.DismissLoadDialog, textinput_update=_textinput, func_on_success=_onSuccess)
        self.popup = Popup(title='File Open Dialog', content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def DismissLoadDialog(self):
        self.popup.dismiss()

    def Load(self, _path, _filename, _textinput, _onSuccess):
        with open(os.path.join(_path, _filename[0])) as stream:
            _textinput.text = stream.read()
            if _onSuccess is not None:
                _onSuccess()
        self.DismissLoadDialog()
    
    def OnSuccessLoadPreprocessCode(self):
        self.root.manager.preprocess_code = self.root.config.textinput_preprocess.text

    def OnSuccessLoadControlCode(self):
        self.root.manager.control_code = self.root.config.textinput_control.text

    def OnSuccessLoadAgentConfig(self):
        self.root.manager.agent_config = json.loads(self.root.config.textinput_agent_config.text)
        self.root.server.button_init_agent.disabled = False

    def OnSuccessLoadNetworkCode(self):
        pass

class LoadDialog(FloatLayout):

    textinput_update = ObjectProperty(None)
    
    func_load = ObjectProperty(None)
    func_cancel = ObjectProperty(None)
    func_on_success = ObjectProperty(None)

class Widget(App):

    def __init__(self, _manager):
        super(Widget, self).__init__()
        self.manager = _manager

    def build(self):
        root = RootWidget(self.manager)
        server = ServerWidget(func_start=root.OnStart, func_stop=root.OnStop)
        config = ConfigWidget()

        root.add_widget(server)
        root.server = server
        server.root = root
        root.add_widget(config)
        root.config = config
        config.root = root

        return root

Factory.register('RootWidget', cls=RootWidget)
Factory.register('ServerWidget', cls=ServerWidget)
Factory.register('ConfigWidget', cls=ConfigWidget)
Factory.register('LoadDialog', cls=LoadDialog)