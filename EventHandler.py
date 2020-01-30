import os
import time
import sys, signal
from gpiozero import Button
import signal
import argparse
import threading
import requests
import json
import schedule

time_when_pressed = 0
doubleclick_time = 500
bounce_time = 50
time_last_released = 0
button = Button(2)


def signal_handler(signal, frame):
    print("\nProgram exiting")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def timer_function():
    print("Timeout occured {0}\n".format(time.strftime("%H:%M:%S")))
    event = {'Timer timeout': time.strftime("%Y-%m-%d %H:%M:%S")}
    post_payload(event)


def post_payload(payload):
    posttime = time.strftime("%Y-%m-%d %H:%M:%S")
    payload.update( {'posted' : posttime} )
    r = requests.post("http://127.0.0.1:8080", json.dumps(payload))
    if r.status_code != 200 :
        print("Posting issue, return code was {0}".format(r.status_code))


def pressed():
    global time_when_pressed

    time_when_pressed = int(round(time.time() * 1000))
    print("Pressed at {0}".format(time_when_pressed))


def released():
    global time_last_released
    global time_when_pressed

    time_when_released = int(round(time.time() * 1000))
    print("Released at {0}".format(time_when_released))
    if (time_when_released - time_when_pressed < bounce_time):
        print("Just a bounce, no event to server")
        time_when_released = 0
        time_last_released = time_when_released
    else:
        print("Longer press")
        if time_last_released + doubleclick_time > time_when_released:
            button_released = {'click': 'doubleclick'}
            post_payload(button_released)
            # Reset both release times
            time_when_released = 0
            print("Longer press - DC ")
        else:
            button_released = {'click': 'singleclick'}
            post_payload(button_released)
            print("Longer press - SC")
        time_last_released = time_when_released
        print("Longer press made, Button released")
          
button.when_pressed = pressed
button.when_released = released

def main():
    global bounce_time
    global doubleclick_time

    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', default=60, help='Time beween status events in s', type=int)
    parser.add_argument('--bounce', default=50, help='Ignoring time for clicks in ms', type=int)
    parser.add_argument('--doubleclick', default=500, help='Time for a secondclick to be registered as doubleclick in ms', type=int)
    args = parser.parse_args()
    # Don't allow shorter bounce time than 30 ms
    bounce_time = max(30, args.bounce)

    print("Entering event loop")
    while True:
        try:
            schedule.every(args.timeout).seconds.do(timer_function)
            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as  e:
                print("Exception was {0}".format(e))
                pass

if __name__ == "__main__":
    main()
