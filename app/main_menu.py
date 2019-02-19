
import kivy
from kivy.uix.label import Label

from manager import Menu
from instruction_menu import InstructionEntryMenu


class MainMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.add_child(InstructionEntryMenu(name='Entry'))




		self.add_widget(Label(text='[b]Main Menu[/b]', markup=True))



	def on_touch_down(self, touch):
		self.switch_to_child('Entry')








	