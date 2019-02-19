
import kivy
from kivy.utils import escape_markup
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label


from manager import Menu


class DefaultsMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		''' Containing widget for this menu '''
		self.base_layout = FloatLayout(size=(200,300))
		self.add_widget(self.base_layout)

		''' Scrollable list of presets '''
		self.scroll_container = ScrollView(size_hint = (1, None), size=(Window.width, Window.height))
		self.base_layout.add_widget(self.scroll_container)
		self.scroll_list = GridLayout(cols=2, size_hint=(1,None))
		self.scroll_list.bind(minimum_height=self.scroll_list.setter('height'))
		self.scroll_container.add_widget(self.scroll_list)

		''' List presets by name. If clicked, show values of this preset
		Navigation button brings them back to instruction menu '''

		self.scroll_list.add_widget(Button(text='test',size_hint_y=None,height=40))
		self.scroll_list.add_widget(Label(text=''))














		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1,.1))
		self.base_layout.add_widget(self.navigation_layout)

		self.back_button = Button(text='<- Back')
		self.navigation_layout.add_widget(self.back_button)
		self.confirm_button = Button(text='Confirm')
		self.navigation_layout.add_widget(self.confirm_button)

		self.back_button.bind(on_press = self.on_back)
		self.confirm_button.bind(on_press = self.on_confirm)






	''' Callbacks '''
	def on_back(self, instance):
		self.switch_to_parent()

	def on_confirm(self, instance):
		# self.parent_menu.time = self.selection.time
		# self.parent_menu.temp = self.selection.temp
		self.on_back(instance)
		...



	def load_presets(self):
		''' For now, a test list '''

		...

