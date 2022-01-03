'''
Created on Sep 29, 2016

@author: user
'''
import logging

class ThreadControll(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-9s) %(message)s',)
                        
    def wait_for_event(self, e):
        logging.debug('wait_for_event starting')
        event_is_set = e.wait()
        logging.debug('event set: %s', event_is_set)
    
    def wait_for_event_timeout(self, e, t):
#         pass
        while not e.isSet():
            logging.debug('wait_for_event_timeout starting')
            event_is_set = e.wait(t)
            logging.debug('event set: %s', event_is_set)
            if event_is_set:
                logging.debug('processing event')
            else:
                logging.debug('doing other things')

        