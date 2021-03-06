import kivy
from kivy.utils import escape_markup, platform
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.clock import Clock

import socket

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object




class Menu(Screen):
	''' Menu object; acts as node in the hierarchy '''

	# static variable; all Menu objects access the same ScreenManager
	_sm = ScreenManager()
	size = Window.size if platform == 'android' else (800,600) 

	# static, read-only variable
	@property
	def sm(self):
		return self._sm

	def __init__(self, name, parent=None, **kwargs):
		super().__init__(**kwargs)
		self.name = name
		self.parent_menu = None
		self.child_menus = {}

	def add_child(self, menu):
		self.child_menus[menu.name] = menu
		menu.parent_menu = self
		self.sm.add_widget(menu)

	def switch_to_parent(self):
		self.sm.transition.direction = 'down'
		self.sm.current = self.parent_menu.name

	def switch_to_child(self, name):
		self.sm.transition.direction = 'up'
		self.sm.current = name

	def on_back(self, button_instance):
		self.switch_to_parent()

	def send(self, s, message):
		''' Send message string to pi '''
		try:
			s.send(message.encode('utf-8'))
		except socket.error:
			print("An error has occurred... couldn't send data")

	def recv(self, c):
		''' Receive data from pi (such as remaining time or current temperature '''
		data = 0
		try:
			data = c.recv(12345).decode()
		except socket.error:
			print("An error has occurred... couldn't send data")
		return data

	def to_minsec(self, seconds):
		''' format seconds as minutes:seconds '''
		minutes, seconds = divmod(int(seconds),60)
		return ':'.join([str(minutes).rjust(2,'0'), str(seconds).rjust(2,'0')])

	def to_sec(self, minsec):
		''' format minutes:seconds as seconds '''
		*minutes, seconds = minsec.split(':')

		if not minutes:
			return int(seconds)
		return int(minutes[0])*60 + int(seconds)

	def just_digits(self, string, include_colon=False):
		''' Remove anything that isn't a digit '''
		if include_colon:
			return ''.join(c for c in string if c in ':0123456789')
		else:
			return ''.join(c for c in string if c in '0123456789')

class RootMenu(Menu):
	''' Welcome/start menu '''

	def __init__(self, **kwargs):
		super().__init__(name='root', **kwargs)
		self.sm.add_widget(self)
		self.add_widget(Label(text='[i]Touch to begin[/i]', markup=True))

	def on_touch_down(self, touch):
		self.switch_to_child('Main')










