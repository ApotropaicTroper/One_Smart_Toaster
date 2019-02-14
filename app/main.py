
import kivy
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from manager import MenuSystem
from main_menu import MainMenu
from instruction_menu import InstructionEntryMenu


class AppBase(App):
	def build(self):
		return manager.sm

if __name__ == '__main__':
	manager = MenuSystem()
	manager.add_menu(MainMenu(name='Main'),  parent='root')
	manager.add_menu(InstructionEntryMenu(name='Entry'), parent='Main')

	AppBase().run()
	# print(manager.menus)
	# print()
