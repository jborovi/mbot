
import time as time_ #make sure we don't override time
def millis():
    return int(round(time_.time() * 1000))