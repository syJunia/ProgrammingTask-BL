import threading
import sys, signal
import time

a_lock = threading.Lock()

def timer_function():
    print("Timeout occured\n")

def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    global restart

    while True:
        try:
            timer = threading.Timer(3.0, timer_function)
            while True:
                print("will sleep")
                time.sleep(1)
                print("slept")
                if not timer.is_alive():
                    timer = threading.Timer(3.0, timer_function)
                    timer.start()
                    print("restarting timer")
        except Exception as  e:
                print("Exception was {0}".format(e))
                pass
    print("Exit\n")

if __name__ == "__main__":
    main()
