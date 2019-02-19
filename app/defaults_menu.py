
import kivy
from kivy.utils import escape_markup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button


from manager import Menu


class DefaultsMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		''' Containing widget for this menu '''
		self.base_layout = FloatLayout(size=(300,300))
		self.add_widget(self.base_layout)

		''' Scrollable list of presets '''
		self.scroll_list = ScrollView(size_hint = (None, .8))

		''' List presets by name. If clicked, show values of this preset
		Navigation button brings them back to instruction menu '''













		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(1,.1))
		self.base_layout.add_widget(self.navigation_layout)

	def load_presets(self):
		''' For now, a test list '''

		...

