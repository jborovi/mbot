import os

tty = os.open('/dev/tty2')
os.write(tty, "TESTTEST")

