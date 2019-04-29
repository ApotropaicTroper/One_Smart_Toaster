import threading as thread
import os


class CookInstructions(object):
    ''' Manage access to cooking parameters '''

    default_time, default_temp = 0, 0
    _cook_time, _cook_temp = 0, 0
    mutex_time, mutex_temp = None, None
    confirmed, stopped = None, None

    def __init__(self, cook_time=0, cook_temp=0):
        self.mutex_time = thread.Lock()
        self.mutex_temp = thread.Lock()

        self.cook_time = cook_time
        self.cook_temp = cook_temp
        # initial state equals not set, as expected
        self.stopped = thread.Event()
        self.confirmed = thread.Event()
        
        
        if os.stat("default.txt").st_size == 0:
            self.cook_time = cook_time
            self.cook_temp = cook_temp
        else:
            with open("default.txt") as f:
                content = f.readlines()
                content = [x.strip() for x in content]
                self.cook_time = int(content[0])
                self.cook_temp = int(content[1])

    @property
    def cook_time(self):
        ''' Read access for cooking time '''

        with self.mutex_time:
            return self._cook_time

    @cook_time.setter
    def cook_time(self, value):
        ''' Write access for cooking time '''
        if value < 0:
            ''' Report time error '''
            ...
            return
        with self.mutex_time:
            self._cook_time = value

    @property
    def cook_temp(self):
        ''' Read access for cooking temperature '''
        with self.mutex_temp:
            return self._cook_temp

    @cook_temp.setter
    def cook_temp(self, value):
        ''' Write access for cooking temperature '''

        if value < 0:
            ''' Report temperature error '''
            ...
            return
        with self.mutex_temp:
            self._cook_temp = value

    def confirm(self):
        ''' User has confirmed submitted instructions '''
        self.confirmed.set()

    def stop(self):
        ''' User wishes to halt the cooking process '''
        self.stopped.set()
        self.confirmed.clear()

    def clear(self):
        ''' Reset all provided settings, and clear all flags '''
        if self.default_time != 0 and self.default_temp != 0:
            self.cook_time = default_time
            self.cook_temp = default_temp
        else:
            self.cook_temp = 0
            self.cook_temp = 0
        self.confirmed.clear()
        self.stopped.clear()
        
    def update_timer(self):
        '''Update the timer mid cook'''
        
    def defaults(self, time, temp):
        default_time = time
        default_temp = temp
        self.cook_time = default_time
        self.cook_temp = default_temp        
