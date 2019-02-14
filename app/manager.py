
import kivy
from kivy.utils import escape_markup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label





class Menu(Screen):
	''' Menu object; acts as node in the hierarchy '''

	def __init__(self, name, parent=None, **kwargs):
		super().__init__(**kwargs)
		self.sm = None
		self.depth = None
		self.name = name
		self.parent_menu = None
		self.child_menus = []

	def add_child(self, menu):
		self.child_menus.append(menu)
		menu.parent_menu = self
		menu.depth = self.depth + 1

	def switch_to_parent(self):
		self.sm.transition.direction = 'down'
		self.sm.current = self.parent_menu.name

	def switch_to_child(self, index):
		self.sm.transition.direction = 'up'
		self.sm.current = self.child_menus[index].name

class RootMenu(Menu):
	''' Welcome/start menu '''

	def __init__(self, **kwargs):
		super().__init__(name='root', **kwargs)
		self.depth = 0
		self.add_widget(Label(text='[i]Touch to begin[/i]', markup=True))

	def on_touch_down(self, touch):
		self.switch_to_child(0)



class MenuSystem(object):
	''' Menu Tree '''


	def __init__(self):
		''' Initialize screen manager and root menu (start screen) '''
		self.menus = {}	# name:widget pairs
		self.sm = ScreenManager()	# direction can be left/right/up/down
		self.root = RootMenu()
		self.add_menu(self.root)

	def add_menu(self, menu, parent=None):
		''' Add a new menu to the manager '''

		menu.sm = self.sm	# grant child access to Screen Manager
		if parent is not None:
			menu.parent_menu = self.menus[parent]
			menu.parent_menu.add_child(menu)

		self.menus[menu.name] = menu


		self.sm.add_widget(menu)



