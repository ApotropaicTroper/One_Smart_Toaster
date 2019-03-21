
import kivy
kivy.require('1.9.1')
from kivy.app import App

from manager import RootMenu
from main_menu import MainMenu


class AppBase(App):
	def build(self):
		root = RootMenu()
		# each Menu creates/destroys its children
		root.add_child(MainMenu(name='Main'))
		return root.sm

if __name__ == '__main__':
	AppBase().run()
