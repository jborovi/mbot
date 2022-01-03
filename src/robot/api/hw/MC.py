from kivy.app import App
from kivy.uix.label import Label
import threading

import time

class ScatterTextWidget(Label):

    def __init__(self,**kwargs):
        self.text = 'nima'
        self.color = [0, 1, 1, 1]
        super(ScatterTextWidget, self).__init__(**kwargs)
a = ScatterTextWidget()

def zaaa():
    import time
    time.sleep(3)
    a.color = [0, 0, 1, 1]
    print "function ran"   

t = threading.Thread(target= zaaa)
t.start()

class TataApp(App):
    def build(self):
        return a


if __name__ == "__main__":
    TataApp().run()