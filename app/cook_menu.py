import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock	# schedule updates to time and temperature display

from manager import Menu
from settings import s

class CookMenu(Menu):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.base_layout = FloatLayout(size=self.size)
		self.add_widget(self.base_layout)

		self.time_label = Label(text='00:00', size_hint=(.4,.2), pos_hint={'x':.3, 'y':.6})
		self.base_layout.add_widget(self.time_label)

		self.temp_label = Label(text='0°C', size_hint=(.4,.2), pos_hint={'x':.3, 'y':.4})
		self.base_layout.add_widget(self.temp_label)

		self.stop_button = Button(text='Stop', size_hint=(.4,.2), pos_hint={'x':.3,'y':.2})
		self.stop_button.bind(on_press = self.on_stop)
		self.base_layout.add_widget(self.stop_button)



		''' Containing widget for user navigation '''
		self.navigation_layout = BoxLayout(orientation='horizontal', spacing=0, size_hint=(.4,.1), pos_hint={'x':.3,'y':0})
		self.base_layout.add_widget(self.navigation_layout)

		self.back_button = Button(text='<- Back')
		self.back_button.bind(on_press=self.on_back)
		self.navigation_layout.add_widget(self.back_button)

	def on_pre_enter(self):
		self.update_event = Clock.schedule_interval(self.update_labels, 0.1)

	def on_leave(self):
		Clock.unschedule(self.update_event)
		self.update = None


	def update_labels(self, dt):
		print('Receive time and temperature data from device')
		# print(self.time_label.text)
		# print(self.to_sec(self.time_label.text))

		self.recv(s)

		self.time_label.text = self.to_minsec(self.to_sec(self.time_label.text)+1)
		self.temp_label.text = ''.join((str(int(self.temp_label.text[:-2])+1),'°C'))



	def on_stop(self, instance):
		''' Send stop message to microcontroller '''
		...
		print('Send stop message to device')
		stop_message = 'stop'
		self.send(s, stop_message)


