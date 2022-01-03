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
        
