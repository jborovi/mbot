from threading import Thread
import time, sys, signal

shutdown_flag = False #used for gracefull shutdown 

def main_loop():
    while not shutdown_flag:
#         collect_data() # contains some print "data" statements
        print 'ticking'
        time.sleep(5)
    print "done (killed)"

def sighandler(signum, frame):
    print 'signal handler called with signal: %s ' % signum
    global shutdown_flag
    shutdown_flag = True

def main(argv=None):
    signal.signal(signal.SIGTERM, sighandler) # so we can handle kill gracefully
    signal.signal(signal.SIGINT, sighandler) # so we can handle ctrl-c
    try:
        Thread(target=main_loop, args=()).start()
    except Exception, reason:
        print reason

if __name__ == '__main__':
    sys.exit(main(sys.argv))