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
from kivy.clock import Clock
from functools import partial

from manager import Menu



class DefaultsMenu(Menu):

	delimeter = '//'

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

		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1,.1))
		self.base_layout.add_widget(self.navigation_layout)

		self.back_button = Button(text='<- Back')
		self.back_button.bind(on_press = self.on_back)
		self.navigation_layout.add_widget(self.back_button)

		self.set_default_button = Button(text='Set Default')
		self.set_default_button.bind(on_press = self.set_default)
		self.navigation_layout.add_widget(self.set_default_button)

		self.chosen_settings = Label(text='', markup=True)
		self.navigation_layout.add_widget(self.chosen_settings)

		self.confirm_button = Button(text='Confirm')
		self.confirm_button.bind(on_press = self.on_confirm)
		self.navigation_layout.add_widget(self.confirm_button)

		self.pick_default = False
		self.index_default = None



	''' Callbacks '''
	def on_pre_enter(self):
		''' Load Presets '''
		with open('presets.txt', mode='r') as f:
			self.presets = [p.strip().split(self.delimeter) for p in f]
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
		for i,p in enumerate(self.presets):
			if 'Default' in p:
				self.index_default = i
				self.on_pick(self.labels[i])

	def on_pick(self, instance):
		''' User chose a preset in the scrollable list '''
		self.chosen_index = self.labels.index(instance)
		self.chosen_settings.text = self.readouts[self.chosen_index].text
		if self.pick_default:
			self.index_default = self.chosen_index

	def on_leave(self):
		''' Save Presets '''
		with open('presets.txt', mode='w') as f:
			for i,p in enumerate(self.presets):
				f.write(self.delimeter.join(p))
				f.write('\n')

		for l,r in zip(self.labels, self.readouts):
			self.scroll_list.remove_widget(l)
			self.scroll_list.remove_widget(r)
		self.scroll_list.remove_widget(self.new)
		del self.labels
		del self.readouts

	def update_cursor(self, instance, dt):
		instance.cursor = len(instance.text.split('\n')[1]), 1

	def set_default(self, instance):
<<<<<<< HEAD
<<<<<<< HEAD
=======
		''' User wishes to set a preset as default '''
>>>>>>> Sperl
=======
		''' User wishes to set a preset as default '''
>>>>>>> Sperl
		self.pick_default = True
		if self.index_default is not None:
			self.presets[self.index_default] = self.presets[self.index_default][:-1]

	def on_new_preset(self, instance):
		''' User is going to add a new preset '''
		self.scroll_list.remove_widget(self.new)
		self.new_settings.text = ''
		self.scroll_list.add_widget(self.new_settings)

	def on_text(self, instance, text):
		''' User is editing presets '''
		check_text = text.split('\n')

		if len(check_text) > 1:
			text = check_text[1]
			text = ''.join(c for c in text if c.isdigit())
			if len(text) > 2:
				text = ':'.join((text[:-2], text[-2:]))
			check_text[1] = text
			if len(check_text) == 2:
				Clock.schedule_once(partial(self.update_cursor, instance), 0)
		if len(check_text) > 2:
			text = check_text[2]
			text = ''.join(c for c in text if c.isdigit())
			check_text[2] = text
		text = '\n'.join(check_text)
		instance.text = text
		if len(check_text) > 3:
			instance.text = '\n'.join(check_text[:3])
			if all(line for line in check_text):
				self.on_set_preset(text)
				self.scroll_list.remove_widget(instance)

	def on_set_preset(self, text):
		''' Add a new preset '''
		settings = text.strip().split('\n')
		name, time, temp = settings
		self.labels.append(Button(text=name,size_hint_y=None,height=50))
		self.readouts.append(Label(text='{}\n{}° '.format(time, temp), size_hint_y=None, height=50))
		self.presets.append([name, str(self.to_sec(time)), temp])

		self.scroll_list.add_widget(self.labels[-1])
		self.scroll_list.add_widget(self.readouts[-1])
		self.scroll_list.add_widget(self.new)


	def on_back(self, instance):
		self.switch_to_parent()

	def on_confirm(self, instance):
		if self.pick_default:
			self.pick_default = False
			self.presets[self.index_default].append('Default')
		else:
			if self.chosen_settings.text != '':
				self.parent_menu.cook_time = self.presets[self.chosen_index][1]
				self.parent_menu.cook_temp = self.presets[self.chosen_index][2]
			self.on_back(instance)




