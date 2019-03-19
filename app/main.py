
import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from manager import RootMenu
from main_menu import MainMenu


class AppBase(App):
	def build(self):
		root = RootMenu()
		# each Menu creates/destroys its children
		root.add_child(MainMenu(name='Main'))
		return root

if __name__ == '__main__':
	AppBase().run()
