
import kivy
from kivy.utils import escape_markup
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from manager import Menu

delimeter = '//'


class DefaultsMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		''' Containing widget for this menu '''
		self.base_layout = FloatLayout(size=(200,300))
		self.add_widget(self.base_layout)

		''' Scrollable list of presets '''
		self.scroll_container = ScrollView(size_hint = (1, None), size=(Window.width, Window.height*.9),pos_hint={'x':0,'y':.1})
		self.base_layout.add_widget(self.scroll_container)
		self.scroll_list = GridLayout(cols=2, size_hint=(1,None))
		self.scroll_container.add_widget(self.scroll_list)
		self.scroll_list.bind(minimum_height=self.scroll_list.setter('height'))

		self.new = Button(text='New Preset', size_hint_y=None, height=50)
		self.new.bind(on_press = self.on_new_preset)
		self.new_settings = TextInput(text='', hint_text='Name\nTime\nTemperature', size_hint_y=None, height=70)
		self.new_settings.bind(on_press = self.on_set_preset)
		self.new_settings.bind(text = self.on_text)


		''' List presets by name. If clicked, show values of this preset
		Navigation button brings them back to instruction menu '''


		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1,.1))
		self.base_layout.add_widget(self.navigation_layout)

		self.back_button = Button(text='<- Back')
		self.navigation_layout.add_widget(self.back_button)

		self.chosen_settings = Label(text='')
		self.navigation_layout.add_widget(self.chosen_settings)

		self.confirm_button = Button(text='Confirm')
		self.navigation_layout.add_widget(self.confirm_button)

		self.back_button.bind(on_press = self.on_back)
		self.confirm_button.bind(on_press = self.on_confirm)


	''' Callbacks '''

	def on_pre_enter(self):
		''' Load Presets '''
		with open('presets.txt', mode='r') as f:
			self.presets = [p.strip().split(delimeter) for p in f]
		# print(self.presets)
		self.names = [p[0] for p in self.presets]
		self.times = [p[1] for p in self.presets]
		self.temperatures = [p[2] for p in self.presets]
		self.labels = [Button(text=n, size_hint_y=None, height=50) for n in self.names]
		for b in self.labels:
			b.bind(on_press = self.on_pick)
		self.readouts = [Label(text='{}\n{}° '.format(self.to_minsec(time), temp), size_hint_y=None, height=50) for name, time, temp in zip(self.names, self.times, self.temperatures)]

		for name, data in zip(self.labels, self.readouts):
			self.scroll_list.add_widget(name)
			self.scroll_list.add_widget(data)
		self.scroll_list.add_widget(self.new)

	def on_pick(self, instance):
		self.chosen_settings.text = self.readouts[self.labels.index(instance)].text


	def on_leave(self):
		''' Save Presets '''
		with open('presets.txt', mode='w') as f:
			for p in self.presets:
				f.write(delimeter.join(p))
				f.write('\n')

		for l,r in zip(self.labels, self.readouts):
			self.scroll_list.remove_widget(l)
			self.scroll_list.remove_widget(r)
		self.scroll_list.remove_widget(self.new)
		del self.labels
		del self.readouts

	def on_new_preset(self, instance):
		''' User is going to add a new preset '''
		self.scroll_list.remove_widget(self.new)
		self.new_settings.text = ''
		self.scroll_list.add_widget(self.new_settings)

	def on_text(self, instance, text):
		''' User is editing presets '''
		if len(text.split('\n')) == 4:
			self.on_set_preset(text)
			self.scroll_list.remove_widget(instance)

	def on_set_preset(self, text):
		''' Add a new preset '''
		# Need check to ensure that time/temperature settings are integers
		settings = text.strip().split('\n')
		name, time, temp = settings
		self.labels.append(Button(text=name,size_hint_y=None,height=50))
		self.readouts.append(Label(text='{}\n{}° '.format(self.to_minsec(time), temp), size_hint_y=None, height=50))
		self.presets.append([name, time, temp])

		self.scroll_list.add_widget(self.labels[-1])
		self.scroll_list.add_widget(self.readouts[-1])
		self.scroll_list.add_widget(self.new)









	def on_back(self, instance):
		self.switch_to_parent()

	def on_confirm(self, instance):
		self.parent_menu.time_input.text, self.parent_menu.temp_input.text = self.chosen_settings.text.split()
		self.on_back(instance)




