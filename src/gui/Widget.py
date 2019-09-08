
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
        self.server.button_start.disabled = True
        self.server.button_stop.disabled = False
        self.server.textinput_ip.disabled = True
        self.manager.ip_server = self.server.textinput_ip.text
        self.server.textinput_port.disabled = True
        self.manager.port_server = int(self.server.textinput_port.text)

        self.config.button_load_preprocess.disabled = True
        self.config.textinput_preprocess.disabled = True
        self.config.button_load_control.disabled = True
        self.config.textinput_control.disabled = True
        self.manager.control_code = self.config.textinput_control.text
        self.config.button_load_keymap.disabled = True
        self.config.textinput_keymap.disabled = True

        t = Thread(target=self.manager.Start)
        t.daemon = True
        t.start()

    def OnStop(self):
        self.server.button_start.disabled = False
        self.server.button_stop.disabled = True
        self.server.textinput_ip.disabled = False
        self.server.textinput_port.disabled = False

        self.config.button_load_preprocess.disabled = False
        self.config.textinput_preprocess.disabled = False
        self.config.button_load_control.disabled = False
        self.config.textinput_control.disabled = False
        self.config.button_load_keymap.disabled = False
        self.config.textinput_keymap.disabled = False

        t = Thread(target=self.manager.Stop)
        t.daemon = True
        t.start()

class ServerWidget(BoxLayout):

    button_start = ObjectProperty(None)
    button_stop = ObjectProperty(None)
    textinput_ip = ObjectProperty(None)
    textinput_port = ObjectProperty(None)

    func_start = ObjectProperty(None)
    func_stop = ObjectProperty(None)

class ConfigWidget(GridLayout):

    button_load_preprocess = ObjectProperty(None)
    button_load_control = ObjectProperty(None)
    button_load_keymap = ObjectProperty(None)
    textinput_preprocess = ObjectProperty(None)
    textinput_control = ObjectProperty(None)
    textinput_keymap = ObjectProperty(None)

    def ShowLoadDialog(self, _textinput):
        content = LoadDialog(func_load=self.Load, func_cancel=self.DismissLoadDialog, textinput_update=_textinput)
        self.popup = Popup(title='Load File', content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def DismissLoadDialog(self):
        self.popup.dismiss()

    def Load(self, _path, _filename, _textinput):
        with open(os.path.join(_path, _filename[0])) as stream:
            _textinput.text = stream.read()
        self.DismissLoadDialog()

class LoadDialog(FloatLayout):

    textinput_update = ObjectProperty(None)
    
    func_load = ObjectProperty(None)
    func_cancel = ObjectProperty(None)

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
        root.add_widget(config)
        root.config = config

        return root

Factory.register('RootWidget', cls=RootWidget)
Factory.register('ServerWidget', cls=ServerWidget)
Factory.register('ConfigWidget', cls=ConfigWidget)
Factory.register('LoadDialog', cls=LoadDialog)