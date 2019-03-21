import kivy
from kivy.uix.floatlayout import FloatLayout

from manager import Menu

class CookMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.base_layout = FloatLayout(size=self.size)

