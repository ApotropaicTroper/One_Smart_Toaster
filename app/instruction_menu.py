

import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from manager import Menu
from defaults_menu import DefaultsMenu
from settings import MenuScreen

class InstructionEntryMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.add_child(DefaultsMenu(name='Defaults'))
		self.add_child(MenuScreen(name='menu'))


		''' Containing widget for this menu '''
		self.base_layout = FloatLayout(size=(200,300))
		self.add_widget(self.base_layout)

		''' Containing widget for user input '''
		self.entry_layout = FloatLayout(size_hint=(1,.9), pos_hint={'x':0,'y':.1})
		self.base_layout.add_widget(self.entry_layout)

		self.entry_layout.add_widget(Label(text='Timer:', size_hint=(.5,None), height=30, pos_hint={'x':0,'y':.8}))
		self.time_input = TextInput(text='', hint_text='00:00', multiline=False, size_hint=(.5,None), height=30, pos_hint={'x':.5,'y':.8})
		self.entry_layout.add_widget(self.time_input)
		self.time_input_error = Label(text='', markup=True, size_hint=(.5,None), height=30, pos_hint={'x':.25,'y':.7})
		self.entry_layout.add_widget(self.time_input_error)

		self.entry_layout.add_widget(Label(text='Temperature:', size_hint=(.5,None), height=30, pos_hint={'x':0,'y':.6}))
		self.temp_input = TextInput(text='', hint_text='', multiline=False, size_hint=(.5,None), height=30, pos_hint={'x':.5,'y':.6})
		self.entry_layout.add_widget(self.temp_input)
		self.temp_input_error = Label(text='', markup=True, size_hint=(.5,None), height=30, pos_hint={'x':.25,'y':.5})
		self.entry_layout.add_widget(self.temp_input_error)

		self.time_input.bind(on_text_validate=self.on_enter_time)
		self.temp_input.bind(on_text_validate=self.on_enter_temp)

		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1,.1))
		self.base_layout.add_widget(self.navigation_layout)

		self.settings_button = Button(text='Settings')
		self.settings_button.bind(on_press=self.to_settings)
		self.back_button = Button(text='<- Back')
		self.back_button.bind(on_press=self.on_back)
		self.defaults_button = Button(text='Defaults ->')
		# self.defaults_button.bind(on_press = self.on_defaults)
		self.navigation_layout.add_widget(self.back_button)
		self.navigation_layout.add_widget(self.settings_button)
		self.navigation_layout.add_widget(self.defaults_button)
		# self.base_layout.add_widget(Label(text='test'))

		self.cook_time = 0
		self.cook_temp = 0


	''' Callbacks '''
	def on_back(self, instance):
		self.switch_to_parent()

	def on_defaults(self, instance):
		self.switch_to_child('Defaults')

	def to_settings(self, instance):
		self.switch_to_child('menu')

	def on_enter_time(self, instance):
		time = self.time_input.text
		if not time.isdigit():
			self.time_input_error.text = '[color=#FF0000]Not a number[/color]'
		elif len(time) > 4:
			self.time_input_error.text = '[color=#FF0000]Too long[/color]'
		else:
			if len(time) > 2:
				minutes = time[:-2]
				seconds = time[-2:]
				self.time_input.text = ' : '.join([minutes,seconds])
				self.cook_time = 60*int(minutes) + int(seconds)
			else:
				self.cook_time = int(time)

	def on_enter_temp(self, instance):
		temp = self.temp_input.text
		if not temp.isdigit():
			self.temp_input_error.text = '[color=#FF0000]Not a number[/color]'
		else:
			self.cook_temp = int(temp)



