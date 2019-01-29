
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
kivy.require('1.10.1')

class AppBase(App):
	def build(self):
		''' Initialize root widget '''
		return MainMenu()

class MainMenu(GridLayout):

	def __init__(self):
		super(MainMenu,self).__init__()
		self.add_widget(Label(text='Hello!'))
		...



AppBase().run()





