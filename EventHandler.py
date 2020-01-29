import os
import time
from gpiozero import Button
import signal
import argparse
import datetime
import threading
import sys, signal
import time
import requests
import json

a_lock = threading.Lock()

def timer_function():
    print("Timeout occured {0}\n".format(datetime.datetime.now()))
    event = {'timeout': time.strftime("%Y-%m-%d %H:%M")}
    post_payload(event)


def signal_handler(signal, frame):
    print("\nProgram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
time_when_pressed = 0
bounce_time = 100

def post_payload(payload):
    posttime = time.strftime("%Y-%m-%d %H:%M")
    payload.update( {'posted' : posttime} )
    r = requests.post("http://127.0.0.1:8080", json.dumps(payload))
    if r.status_code != 200 :
        print("Post Was {0}".format(r.status_code))

def pressed():
    time_when_pressed = int(datetime.datetime.now().timestamp())
    print("Pressed at {0}".format(time_when_pressed))
    #button_pressed = {'button': 'pressed'}
    #post_payload(button_pressed)


def released():
    time_when_released = int(datetime.datetime.now().timestamp())
    print("Released at {0}".format(time_when_released))
    if (time_when_pressed - time_when_released < bounce_time):
        print("Short bounce")
        button_released = {'button': 'released'}
        post_payload(button_released)
    else:
        print("Longer bounce")

button = Button(2)

button.when_pressed = pressed
button.when_released = released

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--bounce', default=100, help='Press time in ms', type=int)
    parser.add_argument('--timeout', default=5, help='Time beween timeout events', type=int)
    args = parser.parse_args()
    bounce_time = min(100, args.bounce)

    #print("Got bounce {0}".format(args.bounce))
    #print("Got timeout {0}".format(args.timeout))

    #start_button_reader()
    #start_background_timer()

    while True:
        try:
            timer = threading.Timer(args.timeout, timer_function)
            while True:
                time.sleep(1)
                if not timer.is_alive():
                    timer = threading.Timer(args.timeout, timer_function)
                    timer.start()
                    #print("restarting timer")
        except Exception as  e:
                print("Exception was {0}".format(e))
                pass

if __name__ == "__main__":
    main()
