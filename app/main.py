
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

from manager import RootMenu
from main_menu import MainMenu


class AppBase(App):
	def build(self):
		return root.sm

if __name__ == '__main__':
	root = RootMenu()
	# each Menu creates/destroys its children
	root.add_child(MainMenu(name='Main'))


	AppBase().run()
