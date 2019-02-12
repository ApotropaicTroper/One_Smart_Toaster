
import kivy
from kivy.app import App
from kivy.utils import escape_markup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
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

	# PageLayout: use for default 
		# self.layout = GridLayout(rows=50,cols=1)
		self.layout = FloatLayout(size=(300,300))
		# self.layout = BoxLayout(orientation='vertical', padding=[10,50,10,50])
		self.add_widget(self.layout)
		# self.layout.add_widget(Label(text=''))

		self.layout.add_widget(Label(text='Timer:', size_hint=(1/3,1/8), pos_hint={'x':.4,'y':.75}))

		self.time_input = TextInput(text='', multiline=False, size_hint=(1/3,1/8), pos_hint={'x':.4,'y':.625})
		self.time_input.bind(on_text_validate=self.on_enter_time)
		self.time_input_confirm = Label(text='', markup=True, size_hint=(1/3,1/8), pos_hint={'x':.4,'y':.5})
		self.layout.add_widget(self.time_input)
		self.layout.add_widget(self.time_input_confirm)

		self.layout.add_widget(Label(text='Temperature:', size_hint=(1/3,1/8), pos_hint={'x':.4,'y':.375}))
		self.temp_input = TextInput(text='', multiline=False, size_hint=(1/3,1/8), pos_hint={'x':.4,'y':.25})
		self.temp_input.bind(on_text_validate=self.on_enter_temp)
		self.temp_input_confirm = Label(text='', markup=True, size_hint=(1/3,1/8), pos_hint={'x':.4,'y':.125})
		self.layout.add_widget(self.temp_input)
		self.layout.add_widget(self.temp_input_confirm)

		self.cook_time = 0
		self.cook_temp = 0


	def on_enter_time(self, instance):
		if not instance.text.isdigit():
			self.time_input_confirm.text = '[i][color=#FF0000]Not a number![/color][/i]'
			return
		if len(instance.text) > 4:
			self.time_input_confirm.text = '[i][color=#FF0000]Too long! (4 digits)[/color][/i]'
			return

	def on_enter_temp(self, instance):
		if not instance.text.isdigit():
			self.temp_input_confirm.text = '[i][color=#FF0000]Not a number![/color][/i]'
			return
		if len(instance.text) > 4:
			self.temp_input_confirm.text = '[i][color=#FF0000]Too long! (4 digits)[/color][/i]'
			return

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





