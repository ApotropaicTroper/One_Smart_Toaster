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
from settings import s

from functools import partial

class DefaultsMenu(Menu):

	delimeter = '//'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		''' Containing widget for this menu '''
		self.base_layout = FloatLayout(size=self.size)
		self.add_widget(self.base_layout)

		''' Scrollable list of presets '''
		self.scroll_container = ScrollView(size_hint=(1, None), size=(self.size[0], self.size[1] * .9),
										   pos_hint={'x': 0, 'y': .1})
		self.base_layout.add_widget(self.scroll_container)
		self.scroll_list = GridLayout(cols=2, size_hint=(1, None))
		self.scroll_container.add_widget(self.scroll_list)
		self.scroll_list.bind(minimum_height=self.scroll_list.setter('height'))

		self.new = Button(text='New Preset', size_hint_y=None, height=self.size[1] // 12)
		self.new.bind(on_press=self.on_new_preset)
		self.new_settings = TextInput(text='', hint_text='Name\nTime\nTemperature (Celsius)', size_hint_y=None,
									  height=self.size[1] // 10)
		self.new_settings.bind(text=self.on_text)
		self.new_settings.bind(text=self.on_text)

		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1, .1))
		self.base_layout.add_widget(self.navigation_layout)

		self.back_button = Button(text='<- Back')
		self.back_button.bind(on_press=self.on_back)
		self.navigation_layout.add_widget(self.back_button)

		self.set_default_button = Button(text='Set Default')
		self.set_default_button.bind(on_press=self.set_default)
		self.navigation_layout.add_widget(self.set_default_button)

		self.chosen_settings = Label(text='', markup=True)
		self.navigation_layout.add_widget(self.chosen_settings)

		self.confirm_button = Button(text='Confirm')
		self.confirm_button.bind(on_press=self.on_confirm)
		self.navigation_layout.add_widget(self.confirm_button)

		self.pick_default = False
		self.index_default = None
		self.time_capped = False  # value used to manage text callback in text callback

	def cursor_update_insert(self, instance, old_cursor, capped, dt):
		''' Move cursor position when colon added to input '''
		old, old_line = old_cursor
		new, new_line = instance.cursor

		if old_line != 1:
			return
		if old_line != new_line:
			return
		check_text = instance.text.split('\n')

		text = check_text[1]

		if len(text) == 2 and old == 3 and new == 2:
			instance.cursor = new - 1, new_line
		elif len(text) == 4 and old == 2 and new == 3:
			instance.cursor = new + 1, new_line
		elif len(text) == 5:
			instance.cursor = old if capped else new, new_line

	''' Callbacks '''
	def on_pre_enter(self):
		''' Load Presets '''
		try:
			with open('presets.txt', mode='r') as f:
				self.presets = [p.strip().split(self.delimeter) for p in f]
		except FileNotFoundError:
			open('presets.txt', mode='x').close()
			self.presets = []
		except IOError:
			open('presets.txt', mode='xx').close()
			self.presets = []
		self.names = [p[0] for p in self.presets]
		self.times = [p[1] for p in self.presets]
		self.temperatures = [p[2] for p in self.presets]
		self.labels = [Button(text=n, size_hint_y=None, height=self.size[1] // 12) for n in self.names]
		for b in self.labels:
			b.bind(on_press=self.on_pick)
		self.readouts = [
			Label(text='{}\n{}° '.format(self.to_minsec(time), temp), size_hint_y=None, height=self.size[1] // 12) for
			name, time, temp in zip(self.names, self.times, self.temperatures)]

		for name, data in zip(self.labels, self.readouts):
			self.scroll_list.add_widget(name)
			self.scroll_list.add_widget(data)
		self.scroll_list.add_widget(self.new)
		for i,p in enumerate(self.presets):
			if 'Default' in p:
				self.index_default = i
				self.on_pick(self.labels[i])
				break

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


	def set_default(self, instance):
		''' User wishes to set a preset as default '''
		self.pick_default = True
		# remove 'Default' label from presets list
		if self.index_default is not None:
			self.presets[self.index_default] = self.presets[self.index_default][:3]
			print(self.presets[self.index_default][1])
		if self.index_default is not None:
			code = 'Default' + ' '
			co_time = str(self.presets[self.index_default][1])
			co_temp = str(self.presets[self.index_default][2])
			data = code + co_time + ' ' + co_temp
			Menu.send(self, s, data)

	def on_new_preset(self, instance):
		''' User is going to add a new preset '''
		self.pick_default = False
		self.scroll_list.remove_widget(self.new)
		self.new_settings.text = ''
		self.scroll_list.add_widget(self.new_settings)

	def on_text(self, instance, text):
		''' User is editing presets '''
		check_text = text.split('\n')
		cursor_col, cursor_line = instance.cursor
		check_text[0] = ''.join(check_text[0].split(self.delimeter))
		if len(check_text) > 1:
			if not self.time_capped:
				self.time_capped = len(check_text[1]) > 5
			text = self.just_digits(check_text[1], False)[-4:]
			if len(text) > 2:
				text = ':'.join((text[:-2], text[-2:]))
			check_text[1] = text
			Clock.schedule_once(partial(self.cursor_update_insert, instance, instance.cursor, self.time_capped))
		if len(check_text) > 2:
			check_text[2] = self.just_digits(check_text[2], False)[-3:]
		if len(check_text) == 4:
			del check_text[cursor_line + 1]
			if all(line for line in check_text):
				self.on_set_preset('\n'.join(check_text))
				self.scroll_list.remove_widget(instance)
				return
		instance.text = '\n'.join(check_text)
		self.time_capped = False

	def on_set_preset(self, text):
		''' Add a new preset '''
		settings = text.strip().split('\n')
		name, time, temp = settings
		if len(time) > 2:
			time = ':'.join((time[:-2], time[-2:]))
		self.labels.append(Button(text=name, size_hint_y=None, height=self.size[1] // 12))
		self.labels[-1].bind(on_press=self.on_pick)
		self.readouts.append(Label(text='{}\n{}° '.format(time, temp), size_hint_y=None, height=self.size[1] // 12))
		self.presets.append([name, str(self.to_sec(time)), temp])

		self.scroll_list.add_widget(self.labels[-1])
		self.scroll_list.add_widget(self.readouts[-1])
		self.scroll_list.add_widget(self.new)



	def on_confirm(self, instance):
		if self.pick_default:
			self.pick_default = False
			if self.index_default is None:
				return
			self.presets[self.index_default].append('Default')
		else:
			if self.chosen_settings.text != '':
				self.parent_menu.cook_time = self.presets[self.chosen_index][1]
				self.parent_menu.cook_temp = self.presets[self.chosen_index][2]
				code = 'Time' + ' '
				c_time = str(self.presets[self.chosen_index][1])
				time_info = code + c_time
				Menu.send(self, s, time_info)
				code = 'Temp' + ' '
				c_temp = str(self.presets[self.chosen_index][2])
				temp_info = code + c_temp
				Menu.send(self, s, temp_info)
			self.on_back(instance)




