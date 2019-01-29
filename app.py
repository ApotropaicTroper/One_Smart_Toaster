
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
	...


class StartMenu(GridLayout):
	def __init__(self, **kwargs):
		super(MainMenu,self).__init__(**kwargs)
		self.rows = 10
		self.add_widget(Label(text='Hello!'))
		self.add_widget(Label(text='Welcome to Smart Toaster'))
		# self.add_widget(Label(text='to'))
		# self.add_widget(Label(text='Smart'))
		# self.add_widget(Label(text='Toaster'))
		self.add_widget(Button(text='\n\nTouch to begin'))


AppBase().run()





