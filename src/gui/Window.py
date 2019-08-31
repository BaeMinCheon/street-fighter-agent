
import kivy.config
import kivy.app
import kivy.uix.button
import kivy.uix.boxlayout
import kivy.uix.textinput

Config = kivy.config.Config
App = kivy.app.App
Button = kivy.uix.button.Button
BoxLayout = kivy.uix.boxlayout.BoxLayout
TextInput = kivy.uix.textinput.TextInput

Config.set('input', 'mouse', 'mouse,disable_multitouch')

class RootWidget(BoxLayout):

    def __init__(self, _manager):
        super(RootWidget, self).__init__()
        self.manager = _manager
        self.manager.widget = self

        self.orientation = 'vertical'
        self.spacing = 10

class ControlWidget(BoxLayout):

    def __init__(self, _manager):
        super(ControlWidget, self).__init__()
        self.manager = _manager

        self.spacing = 10

        self.b1 = Button(text='Server Start')
        self.b1.on_press = self.manager.OnClickStart
        self.add_widget(self.b1)

        self.b2 = Button(text='Server Stop')
        self.b2.on_press = self.manager.OnClickStop
        self.add_widget(self.b2)

class ConfigWidget(BoxLayout):

    def __init__(self, _manager):
        super(ConfigWidget, self).__init__()
        self.manager = _manager

        self.spacing = 10

        self.tb1 = TextInput(text='# Empty')
        self.add_widget(self.tb1)
        self.tb1.text = self.manager.control_code

        self.b3 = Button(text='Update Code')
        self.b3.on_press = self.manager.UpdateCode
        self.add_widget(self.b3)

class Window(App):

    def __init__(self, _manager):
        super(Window, self).__init__()
        self.manager = _manager

    def build(self):
        root = RootWidget(self.manager)
        root.add_widget(ControlWidget(self.manager))
        root.add_widget(ConfigWidget(self.manager))
        return root