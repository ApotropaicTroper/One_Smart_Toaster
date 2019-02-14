
import kivy
from kivy.uix.label import Label

from manager import Menu

class MainMenu(Menu):


	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(Label(text='[b]Main Menu[/b]', markup=True))













	