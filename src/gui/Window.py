
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

        self.b1 = Button(text='Server Start', size_hint=(1.0, 0.5))
        self.b1.on_press = self.manager.OnClickStart
        self.add_widget(self.b1)

        self.b2 = Button(text='Server Stop',  size_hint=(1.0, 0.5))
        self.b2.on_press = self.manager.OnClickStop
        self.add_widget(self.b2)

        self.tb1 = TextInput(text='# Empty', size_hint=(1.0, 0.5))
        self.add_widget(self.tb1)
        self.manager.UpdateCode()

        self.b3 = Button(text='Update Code')
        self.b3.on_press = self.manager.UpdateCode
        self.add_widget(self.b3)

class Window(App):

    def __init__(self, _manager):
        super(Window, self).__init__()
        self.manager = _manager

    def build(self):
        return RootWidget(self.manager)