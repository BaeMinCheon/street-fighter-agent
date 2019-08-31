
import kivy.config
import kivy.app
import kivy.uix.button
import kivy.uix.boxlayout
import kivy.uix.gridlayout
import kivy.uix.textinput

Config = kivy.config.Config
App = kivy.app.App
Button = kivy.uix.button.Button
BoxLayout = kivy.uix.boxlayout.BoxLayout
GridLayout = kivy.uix.gridlayout.GridLayout
TextInput = kivy.uix.textinput.TextInput

Config.set('input', 'mouse', 'mouse,disable_multitouch')

class RootWidget(BoxLayout):

    def __init__(self, _manager):
        super(RootWidget, self).__init__()
        self.manager = _manager
        self.manager.widget = self
        self.control = None
        self.config = None

        self.orientation = 'vertical'
        self.spacing = 10

class ControlWidget(BoxLayout):

    def __init__(self, _manager):
        super(ControlWidget, self).__init__()
        self.manager = _manager
        self.socket = None

        self.spacing = 10

        self.button_start = Button(text='Server Start')
        self.button_start.on_press = self.manager.OnClickStart
        self.add_widget(self.button_start)

        self.button_stop = Button(text='Server Stop')
        self.button_stop.on_press = self.manager.OnClickStop
        self.add_widget(self.button_stop)

class SocketWidget(GridLayout):

    def __init__(self, _manager):
        super(SocketWidget, self).__init__()
        self.manager = _manager

        self.cols = 2
        self.spacing = 10

        self.textinput_ip = TextInput(text='127.0.0.1')
        self.add_widget(self.textinput_ip)
        
        self.button_ip = Button(text='Update IP')
        self.button_ip.on_press = self.manager.UpdateIP
        self.add_widget(self.button_ip)

        self.textinput_port = TextInput(text='7000')
        self.add_widget(self.textinput_port)

        self.button_port = Button(text='Update Port')
        self.button_port.on_press = self.manager.UpdatePort
        self.add_widget(self.button_port)

class ConfigWidget(BoxLayout):

    def __init__(self, _manager):
        super(ConfigWidget, self).__init__()
        self.manager = _manager

        self.spacing = 10

        self.textinput_control = TextInput(text='# Empty')
        self.add_widget(self.textinput_control)
        self.textinput_control.text = self.manager.control_code

        self.button_update = Button(text='Update Code')
        self.button_update.on_press = self.manager.UpdateCode
        self.add_widget(self.button_update)

class Window(App):

    def __init__(self, _manager):
        super(Window, self).__init__()
        self.manager = _manager

    def build(self):
        root = RootWidget(self.manager)
        control = ControlWidget(self.manager)
        socket = SocketWidget(self.manager)
        config = ConfigWidget(self.manager)

        root.add_widget(control)
        root.control = control
        root.add_widget(config)
        root.config = config

        control.add_widget(socket)
        control.socket = socket

        return root