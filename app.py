
import kivy
from kivy.app import App
from kivy.utils import escape_markup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
# from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

kivy.require('1.10.1')

'''
							Start Menu
							Main Menu
	Instruction Entry Menu				Database Menu
Input Menu		Defaults Menu

'''

class StartMenu(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(Label(text='[i]Touch to begin[/i]', markup=True))

	# overridden method
	def on_touch_down(self, touch):
		sm.transition.direction = 'up'
		sm.current = 'Main'


class MainMenu(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(Label(text='[b]Main Menu[/b]', markup=True))
	def on_touch_down(self, touch):
		sm.transition.direction = 'up'
		sm.current = 'Instruction'


class InstructionEntryMenu(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.layout = GridLayout(rows=5, cols=1)
		self.add_widget(self.layout)
		self.layout.add_widget(Label(text='test_layout_1'))
		self.layout.add_widget(Label(text='test_layout_2'))
		self.time_input = TextInput(text='time_input', multiline=False)
		self.layout.add_widget(self.time_input)

	
	# @staticmethod
	# def on_enter(instance,value):
	# 	print('testing on_enter')

	# def on_touch_down(self, touch):
	# 	print(touch.pos)
	# 	sm.transition.direction = 'down'
	# 	# sm.current = 'Main'

sm = ScreenManager()	# direction can be left/right/up/down
# sm.add_widget(StartMenu(name='Start'))
# sm.add_widget(MainMenu(name='Main'))
sm.add_widget(InstructionEntryMenu(name='Instruction'))

class AppBase(App):
	def build(self):
		return sm

if __name__ == '__main__':
	AppBase().run()





