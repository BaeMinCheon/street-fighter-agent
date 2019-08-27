
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

        self.tb1 = TextInput(text='''# write code to control the game

_data['P1.Position.Y'] = 192 - _data['P1.Position.Y.Raw']
if _data['P1.IsAttacking.Raw'] >= 256:
    _data['P1.IsAttacking'] = 1
else:
    _data['P1.IsAttacking'] = 0
if _data['P1.IsHitting.Raw'] > 256:
    _data['P1.IsHitting'] = 1
else:
    _data['P1.IsHitting'] = 0
if (_data['P1.IsAttacking'] + _data['P1.IsHitting']) == 0:
    _data['P1.CanControl'] = 1
else:
    _data['P1.CanControl'] = 0
_data['P2.Position.Y'] = 192 - _data['P2.Position.Y.Raw']
if _data['P1.Position.X'] > _data['P2.Position.X']:
    _data['P1.IsLeft'] = 1
else:
    _data['P1.IsLeft'] = 0
_data['Gap.X'] = abs(_data['P1.Position.X'] - _data['P2.Position.X'])
_data['Gap.Y'] = abs(_data['P1.Position.Y'] - _data['P2.Position.Y'])
_data['Gap.HP.P1'] = _data['P1.HP.Current'] - _data['P2.HP.Current']
if _data['P1.CanControl'] > 0:
    _data['P1.CanAction'] = 1
    if _data['P1.Position.Y'] == 0:
        _data['P1.CanMove'] = 1
    else:
        _data['P1.CanMove'] = 0
else:
    _data['P1.CanAction'] = 0
    _data['P1.CanMove'] = 0
if _data['Winner.Player.Raw'] > 0:
    _data['Winner.Player'] = 1
else:
    _data['Winner.Player'] = 0
_data['Winner.Player']
if (_data['RoundTimer'] == 0) or (_data['Winner.Player'] > 0):
    if(self.count_frame >= 60):
        self.count_frame = 0
        control = [0, 0, 2]
    else:
        control = [0, 0, 0]''', size_hint=(1.0, 0.5))
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