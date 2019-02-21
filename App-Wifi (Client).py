from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import subprocess
import socket
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: "vertical"

<SettingsScreen>:
    BoxLayout:
        orientation: "vertical"
        Button:
            text: 'Scan For Networks'
            on_release:
                root.manager.current = 'networks'
                root.scan()


        Button:
            text: 'Back to menu'
            on_release:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'

<NetworksScreen>:
    BoxLayout:
        orientation: "vertical"
""")

ssids = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Declare both screens
class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        vLayout2 = BoxLayout(orientation='vertical')
        self.add_widget(vLayout2)

        settings_button = Button(text='Settings')
        vLayout2.add_widget(settings_button)
        settings_button.bind(on_press=self.forwardFunction)

        test_button = Button(text='Test')
        vLayout2.add_widget(test_button)
        test_button.bind(on_press=self.forwardFunction2)

        quit_button = Button(text='Quit')
        vLayout2.add_widget(quit_button)
        quit_button.bind(on_press=self.closeButton)

    def closeButton(self, placeholder):
        s.close()
        App.get_running_app().stop()

    def forwardFunction(self, next_screen):
        sm.transition.direction = 'left'
        sm.current = 'settings'

    def forwardFunction2(self, next_screen):
        sm.transition.direction = 'left'
        sm.current = 'testing'



class TestScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        vLayout3 = BoxLayout(orientation='vertical')
        self.add_widget(vLayout3)
        test_button = Button(text='Send Message',pos = (100,25), size=(100, 25), size_hint=(.15, None))
        self.add_widget(test_button)
        test_button.bind(on_press=self.sendData)
        back_button = Button(text='Back to Menu', size=(100, 25), size_hint=(.15, None))
        vLayout3.add_widget(back_button)
        back_button.bind(on_press=self.backFunction)


    def sendData(self, placeholder):
        data = 'Test Worked'
        try:
            s.send(data.encode('utf-8'))
        except socket.error:
            print("An error has occurred... closing connection to server")
        finally:
            s.shutdown(socket.SHUT_RDWR)
            s.close()


    def backFunction(self, next_screen):
        sm.transition.direction = 'right'
        sm.current = 'menu'

class NetworksScreen(Screen):
    #def settings_release(self):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def backFunction(self, next_screen):
        sm.transition.direction = 'right'
        sm.current = 'settings'

    def connectWifi(self, placeholder):
        #s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 12345  # Reserve a port for your service.

        try:
            s.connect((host, port))
            print(s.recv(1024))
        except socket.error:
            print("An error has occurred... closing connection to server")
        finally:
            s.shutdown(socket.SHUT_RDWR)
            s.close()


    def printButtons(self):
        y = 0
        s2 = self.manager.get_screen('settings')
        vLayout = BoxLayout(orientation='vertical')
        self.add_widget(vLayout)
        while y < len(ssids) - 1:
            button = Button(text=ssids[y])
            button.bind(on_press=self.connectWifi)
            vLayout.add_widget(button)
            y += 1

        back_button = Button(text='Back to Settings')
        vLayout.add_widget(back_button)
        back_button.bind(on_press=self.backFunction)

class SettingsScreen(Screen):

    def scan(self):

        results = subprocess.check_output(["netsh", "wlan", "show", "network"])
        results = results.decode("ascii")  # needed in python 3
        results = results.replace("\r", "")
        ls = results.split("\n")
        ls = ls[4:]
        x = 0
        y = 0

        while x < len(ls):
            if x % 5 == 0:
                ssids.append(ls[x])
            x += 1

        while y < len(ssids)-1:
            y += 1

        s2 = self.manager.get_screen('networks')
        s2.printButtons()


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(TestScreen(name='testing'))
sm.add_widget(NetworksScreen(name='networks'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
