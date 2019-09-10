
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

    def ShowLoadDialog(self, _textinput, _onSuccess = None):
        content = LoadDialog(func_load=self.Load, func_cancel=self.DismissLoadDialog, textinput_update=_textinput, func_on_success=_onSuccess)
        self.popup = Popup(title='File Open Dialog', content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def ShowSaveDialog(self, _onSuccess = None):
        content = SaveDialog(func_save=self.Save, func_cancel=self.DismissLoadDialog, func_on_success=_onSuccess)
        self.popup = Popup(title='File Save Dialog', content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def DismissLoadDialog(self):
        self.popup.dismiss()

    def Load(self, _path, _filename, _textinput, _onSuccess):
        with open(os.path.join(_path, _filename[0])) as stream:
            text = stream.read()
            path = stream.name
            if _textinput is not None:
                _textinput.text = text
            if _onSuccess is not None:
                _onSuccess(path, text)
        self.DismissLoadDialog()
    
    def Save(self, _path, _filename, _onSuccess):
        with open(os.path.join(_path, _filename), 'w') as stream:
            path = stream.name
            if _onSuccess is not None:
                _onSuccess(path)
        self.DismissLoadDialog()

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

    def OnClickStartServer(self):
        self.button_start_server.disabled = True
        self.button_stop_server.disabled = False
        self.button_init_agent.disabled = True
        self.button_load_network.disabled = True
        self.button_save_network.disabled = True
        self.textinput_ip.disabled = True
        self.root.manager.server.ip_server = self.textinput_ip.text
        self.textinput_port.disabled = True
        self.root.manager.server.port_server = int(self.textinput_port.text)

        self.root.config.button_load_preprocess.disabled = True
        self.root.config.textinput_preprocess.disabled = True
        self.root.config.button_load_control.disabled = True
        self.root.config.textinput_control.disabled = True
        self.root.config.button_load_agent_config.disabled = True
        self.root.config.textinput_agent_config.disabled = True
        self.root.config.button_load_network.disabled = True
        self.root.config.textinput_network.disabled = True

        t = Thread(target=self.root.manager.Start)
        t.daemon = True
        t.start()

    def OnClickStopServer(self):
        self.button_start_server.disabled = False
        self.button_stop_server.disabled = True
        self.button_init_agent.disabled = False
        self.button_load_network.disabled = False
        self.button_save_network.disabled = False
        self.textinput_ip.disabled = False
        self.textinput_port.disabled = False

        self.root.config.button_load_preprocess.disabled = False
        self.root.config.textinput_preprocess.disabled = False
        self.root.config.button_load_control.disabled = False
        self.root.config.textinput_control.disabled = False
        self.root.config.button_load_agent_config.disabled = False
        self.root.config.textinput_agent_config.disabled = False
        self.root.config.button_load_network.disabled = False
        self.root.config.textinput_network.disabled = False

        t = Thread(target=self.root.manager.Stop)
        t.daemon = True
        t.start()

    def OnClickInitializeAgent(self):
        self.root.manager.InitAgent()
        self.button_start_server.disabled = False
        self.button_load_network.disabled = False
        self.button_save_network.disabled = False

    def OnSuccessLoadNetwork(self, _path, _text):
        self.root.manager.LoadNetwork(_path)

    def OnSuccessSaveNetwork(self, _path):
        self.root.manager.SaveNetwork(_path)

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

    def OnSuccessLoadPreprocessCode(self, _path, _text):
        self.root.manager.preprocess_code = _text

    def OnSuccessLoadControlCode(self, _path, _text):
        self.root.manager.control_code = _text

    def OnSuccessLoadAgentConfig(self, _path, _text):
        self.root.manager.agent_config = json.loads(_text)
        self.root.server.button_init_agent.disabled = False

    def OnSuccessLoadNetworkCode(self, _path, _text):
        pass

class LoadDialog(FloatLayout):

    textinput_update = ObjectProperty(None)
    
    func_load = ObjectProperty(None)
    func_cancel = ObjectProperty(None)
    func_on_success = ObjectProperty(None)

class SaveDialog(FloatLayout):

    textinput_select = ObjectProperty(None)

    func_save = ObjectProperty(None)
    func_cancel = ObjectProperty(None)
    func_on_success = ObjectProperty(None)

class Widget(App):

    def __init__(self, _manager):
        super(Widget, self).__init__()
        self.manager = _manager

    def build(self):
        root = RootWidget(self.manager)
        server = ServerWidget()
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