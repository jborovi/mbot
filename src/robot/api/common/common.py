'''
Created on Jul 4, 2016

@author: user
'''

class Common(object):
    '''
    classdocs
    '''

    @staticmethod
    def tty_print(text, tty_path='/dev/tty2', color='white', newDialog=False):
        #right now everything is comented out and only simple print is used, 
        #you can change the behaviour and print the output to different console and use colored output if needed
        #
        print text
        
#         import os
#         from termcolor import colored
#         tty = os.open(tty_path, os.O_RDWR)
#         if newDialog:
#             os.write(tty,'\n'*100)
#         os.write(tty, colored("\n\t\t\t\t\t\t\t\t\t\t\t"+text+"\n", color, attrs=['bold'])) # in main thread


        
