'''
Created on Jun 9, 2016

@author: user
'''
import RPi.GPIO as GPIO
import time

class GPIO_controll(object):
    '''
    classdocs
    '''


    debugFalseOn = False
    
    debugFalseOnStarted = None
    
    timeDebug = None

    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(pin,GPIO.IN)
#         
    def checkBtn(self):
#         return GPIO.input(self.pin)
        while True:
# 	    GPIO.output(self.pin,False)
 
            if (GPIO.input(self.pin)):
                print "Button not Pressed"
            else:
                print "Button pressed"
            time.sleep(1)
            
            
    def is_on(self):
#         return True  
# 	self.__check_debug_on()     
#         return self.debugFalseOn
        return not GPIO.input(self.pin)

    def __check_debug_on(self):
        import time
#         print self.debugFalseOnStarted
        
        if self.debugFalseOn:
#             print time.time() - self.debugFalseOnStarted
            if (time.time() - self.debugFalseOnStarted) > self.timeDebug:
                self.debugFalseOn=False
    
#     def set

    def setDebugFalseOnFor(self, debugForSec):
        self.debugFalseOnStarted= time.time()
        self.timeDebug = debugForSec
        self.debugFalseOn = True
        
        
    
    def change_status(self, value):
	pass
#        GPIO.output(self.pin,value)
        
if __name__ == '__main__':
#2 tlacitko
#10 dioda
    btn = GPIO_controll(10)
    btn.checkBtn()
        
