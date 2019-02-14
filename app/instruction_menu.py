
import kivy
from kivy.utils import escape_markup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from manager import Menu

class InstructionEntryMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	# PageLayout: use for default 
		# self.layout = GridLayout(rows=50,cols=1)
		self.base_layout = FloatLayout(size=(300,300))
		self.add_widget(self.base_layout)
		self.entry_layout = FloatLayout(size_hint=(1,.9), pos_hint={'x':0,'y':.1})
		self.base_layout.add_widget(self.entry_layout)
		# self.entry_layout.add_widget(Button(text='test', pos_hint={'x':0,'y':0}))


		# self.layout = BoxLayout(orientation='vertical', padding=[10,50,10,50])
		# self.add_widget(self.layout)
		self.entry_layout.add_widget(Button(text='Timer:', size_hint=(.5,None), height=30, pos_hint={'x':0,'y':.8}))
		self.time_input = TextInput(text='', hint_text='00:00', multiline=False, size_hint=(.5,None), height=30, pos_hint={'x':.5,'y':.8})
		self.entry_layout.add_widget(self.time_input)
		self.time_input_confirm = Label(text='', markup=True, size_hint=(.5,None), height=30, pos_hint={'x':.25,'y':.7})
		self.entry_layout.add_widget(self.time_input_confirm)



		self.entry_layout.add_widget(Button(text='Temperature:', size_hint=(.5,None), height=30, pos_hint={'x':0,'y':.6}))
		self.temp_input = TextInput(text='', hint_text='', multiline=False, size_hint=(.5,None), height=30, pos_hint={'x':.5,'y':.6})
		self.entry_layout.add_widget(self.temp_input)
		self.temp_input_confirm = Label(text='', markup=True, size_hint=(.5,None), height=30, pos_hint={'x':.25,'y':.5})
		self.entry_layout.add_widget(self.temp_input_confirm)




		self.time_input.bind(on_text_validate=self.on_enter_time)








		# self.layout.add_widget(self.time_input)
		# self.layout.add_widget(self.time_input_confirm)

		# self.temp_input.bind(on_text_validate=self.on_enter_temp)
		# self.layout.add_widget(self.temp_input)
		# self.layout.add_widget(self.temp_input_confirm)


		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1,.1))
		self.base_layout.add_widget(self.navigation_layout)

		self.back_button = Button(text='<- Back')
		self.back_button.bind(on_press = self.on_back)
		self.defaults_button = Button(text='Defaults ->')
		# self.defaults_button.bind(on_press = self.on_defaults)
		self.navigation_layout.add_widget(self.back_button)
		self.navigation_layout.add_widget(self.defaults_button)
		# self.base_layout.add_widget(Label(text='test'))

		self.cook_time = 0
		self.cook_temp = 0



	def on_back(self, instance):
		self.switch_to_parent()


	def on_enter_time(self, instance):
		print('time')


	# ''' Callbacks '''
	# def on_back(self, instance):
	# 	sm.transition.direction = 'down'
	# 	sm.current = 'Main'

	# def on_defaults(self, instance):
	# 	sm.transition.direction = 'left'
	# 	sm.current = 'Start'

	# def on_enter_time(self, instance):
	# 	if not instance.text.isdigit():
	# 		self.time_input_confirm.text = '[i][color=#FF0000]Not a number![/color][/i]'
	# 		return
	# 	if len(instance.text) > 4:
	# 		self.time_input_confirm.text = '[i][color=#FF0000]Too long! (4 digits)[/color][/i]'
	# 		return

	# def on_enter_temp(self, instance):
	# 	if not instance.text.isdigit():
	# 		self.temp_input_confirm.text = '[i][color=#FF0000]Not a number![/color][/i]'
	# 		return
	# 	if len(instance.text) > 4:
	# 		self.temp_input_confirm.text = '[i][color=#FF0000]Too long! (4 digits)[/color][/i]'
	# 		return
