
import kivy.config
import kivy.app
import kivy.uix.button
import kivy.uix.boxlayout

Config = kivy.config.Config
App = kivy.app.App
Button = kivy.uix.button.Button
BoxLayout = kivy.uix.boxlayout.BoxLayout

Config.set('input', 'mouse', 'mouse,disable_multitouch')

class RootWidget(BoxLayout):

    def __init__(self, _manager):
        super(RootWidget, self).__init__()

        self.b1 = Button(text='Server Start')
        self.b1.on_press = _manager.OnClickStart
        self.add_widget(self.b1)

        self.b2 = Button(text='Server Stop')
        self.b2.on_press = _manager.OnClickStop
        self.add_widget(self.b2)

class Window(App):

    def __init__(self, _manager):
        super(Window, self).__init__()
        self.manager = _manager

    def build(self):
        return RootWidget(self.manager)