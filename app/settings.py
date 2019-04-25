from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

import subprocess
import socket

from manager import Menu

ssids = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.1.89'  # Raspberry Pi ip
# host = '10.16.2.156'
port = 12345  # Reserve a port for your service.

# Declare both screens
class MenuScreen(Menu):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

        vLayout2 = BoxLayout(orientation='vertical')
        self.add_widget(vLayout2)

        settings_button = Button(text='Settings')
        vLayout2.add_widget(settings_button)
        settings_button.bind(on_press=self.forwardFunction)

        back_button = Button(text='Back Home')
        vLayout2.add_widget(back_button)
        back_button.bind(on_press=self.on_back)

    def on_back(self, instance):
        self.switch_to_parent()

    def forwardFunction(self, next_screen):
        self.switch_to_child('settings')

    def forwardFunction2(self, next_screen):
        self.switch_to_child('testing')

class SettingsScreen(Menu):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        vLayout = BoxLayout(orientation='vertical')
        self.add_widget(vLayout)
        scan_button = Button(text='Scan For Networks')
        vLayout.add_widget(scan_button)
        scan_button.bind(on_press=self.to_networks)
        #disconnect_button = Button(text='Disconnect WiFi')
        #vLayout.add_widget(disconnect_button)
        # back_button.bind(on_press=self.remove_widget(vLayout))
        # disconnect_button.bind(on_press=self.disconnectFunction)
        back_button = Button(text='Back Home')
        vLayout.add_widget(back_button)
        back_button.bind(on_press=self.backFunction)

    def to_networks(self, next_screen):
        self.scan()
        self.switch_to_child('networks')

    def disconnectFunction(self, next_screen):
        code = 'Disconnect' + ' '
        placeholder = '0'
        disconnect_info = code + placeholder
        try:
            Menu.send(self, s, disconnect_info)
        except socket.error:
            print("Disconnected from server.")

    def backFunction(self, next_screen):
        self.switch_to_parent()

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

        while y < len(ssids) - 1:
            y += 1

        print(ssids)
        s2 = self.manager.get_screen('networks')
        s2.printButtons(True)
        # p = NetworksScreen.printButtons(self)



class NetworksScreen(Menu):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)

    def backFunction(self, next_screen):
        self.printButtons(False)
        self.switch_to_parent()

    def connectWifi(self):
        try:
            s.connect((host, port))
            print(s.recv(1024))
        except socket.error:
            print("An error has occurred... closing connection to server")
            s.close()
        finally:
            print("")
            #s.shutdown(socket.SHUT_RDWR)
            #s.close()


    def printButtons(self, trigger):
        vLayout = BoxLayout(orientation='vertical')
        self.add_widget(vLayout)
        if trigger == True:
            y = 0
            while y < len(ssids) - 1:
                self.button = Button(text=ssids[y])
                self.button.bind(on_press=NetworksScreen.connectWifi)
                vLayout.add_widget(self.button)
                y += 1

            self.back_button = Button(text='Back Home')
            vLayout.add_widget(self.back_button)
            # back_button.bind(on_press=self.remove_widget(vLayout))
            self.back_button.bind(on_press=self.backFunction)

        elif trigger == False:
            self.remove_widget(self.button)
            self.remove_widget(self.back_button)
            ssids.clear()




