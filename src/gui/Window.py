
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

        self.b1 = Button(text='Server Start')
        self.b1.on_press = _manager.OnClickStart
        self.add_widget(self.b1)

        self.b2 = Button(text='Server Stop')
        self.b2.on_press = _manager.OnClickStop
        self.add_widget(self.b2)

        self.tb1 = TextInput(text='''# write code controlling the game
control = []
if(_data['timer'] == 0):
    if(self.count_frame >= 100):
        self.count_frame = 0
        control = [0, 0, 2]
    else:
        control = [0, 0, 0]
return control
        ''')
        self.add_widget(self.tb1)

class Window(App):

    def __init__(self, _manager):
        super(Window, self).__init__()
        self.manager = _manager

    def build(self):
        return RootWidget(self.manager)