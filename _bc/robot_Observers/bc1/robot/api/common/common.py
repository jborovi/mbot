'''
Created on Jul 4, 2016

@author: user
'''

class Common(object):
    '''
    classdocs
    '''

    @staticmethod
    def tty_print(text, tty_path='/dev/tty2', newDialog=True):
#         import os
#         from termcolor import colored
#         
#         tty = os.open(tty_path, os.O_RDWR)
#         
# 
#         os.system('clear')
#         os.write(tty, colored('--------------------------------------------------------', 'yellow'))
#         
#         os.write(tty, text) # in main thread
#         
#         os.write(tty, colored('--------------------------------------------------------', 'yellow'))
        print text
        
        
class Observer():
    _observers = []
    def __init__(self):
        self._observers.append(self)
        self._observables = {}
    def observe(self, event_name, callback):
        self._observables[event_name] = callback


class Event():
    def __init__(self, name, data, autofire = True):
        self.name = name
        self.data = data
        if autofire:
            self.fire()
    def fire(self):
        for observer in Observer._observers:
            if self.name in observer._observables:
                observer._observables[self.name](self.data)
        
