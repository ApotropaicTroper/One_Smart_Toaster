
import kivy
kivy.require('1.9.1')
from kivy.app import App

from manager import RootMenu
from instruction_menu import InstructionMenu


class AppBase(App):
	def build(self):
		root = RootMenu()
		# each Menu creates/destroys its children
		root.add_child(InstructionMenu(name='Main'))
		return root.sm

if __name__ == '__main__':
	AppBase().run()
	