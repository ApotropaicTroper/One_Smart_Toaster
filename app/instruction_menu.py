
import kivy
from kivy.utils import escape_markup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from manager import Menu


class InstructionEntryMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	# PageLayout: use for default 
		# self.layout = GridLayout(rows=50,cols=1)
		self.layout = FloatLayout(size=(300,300))
		# self.layout = BoxLayout(orientation='vertical', padding=[10,50,10,50])
		self.add_widget(self.layout)

		self.layout.add_widget(Label(text='Timer:', size_hint=(1/3,1/16), pos_hint={'x':.4,'y':.7}))

		self.time_input = TextInput(text='', multiline=False, size_hint=(1/3,1/16), pos_hint={'x':.4,'y':.6})
		self.time_input.bind(on_text_validate=self.on_enter_time)
		self.time_input_confirm = Label(text='', markup=True, size_hint=(1/3,1/16), pos_hint={'x':.4,'y':.5})
		self.layout.add_widget(self.time_input)
		self.layout.add_widget(self.time_input_confirm)

		self.layout.add_widget(Label(text='Temperature:', size_hint=(1/3,1/16), pos_hint={'x':.4,'y':.4}))
		self.temp_input = TextInput(text='', multiline=False, size_hint=(1/3,1/16), pos_hint={'x':.4,'y':.3})
		self.temp_input.bind(on_text_validate=self.on_enter_temp)
		self.temp_input_confirm = Label(text='', markup=True, size_hint=(1/3,1/16), pos_hint={'x':.4,'y':.2})
		self.layout.add_widget(self.temp_input)
		self.layout.add_widget(self.temp_input_confirm)

		self.back_button = Button(text='<-', size_hint=(1/10,1/16), pos_hint={'x':0,'y':0})
		self.back_button.bind(on_press = self.on_back)
		self.layout.add_widget(self.back_button)

		self.defaults_button = Button(text='Defaults', size_hint=(1/10,1/16), pos_hint={'x':.1,'y':0})
		self.defaults_button.bind(on_press = self.on_defaults)
		self.layout.add_widget(self.defaults_button)

		self.cook_time = 0
		self.cook_temp = 0

	''' Callbacks '''
	def on_back(self, instance):
		sm.transition.direction = 'down'
		sm.current = 'Main'

	def on_defaults(self, instance):
		sm.transition.direction = 'left'
		sm.current = 'Start'

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
