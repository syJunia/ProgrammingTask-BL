#### Initial version of a program solving this problem:

An application in python that runs on a raspberry pi that can detect events from a button connected to a GPIO pin and create a message in json format and send it to a “cloud server” using a REST interface and save the data in a file on the server. The application should also send status message at regular intervals to the server e.g. the current time.
For test: The server could be a local server that can receive the messages and save them in a file.

The button handling should handle contact bouncing and be able to detect different button events such as click, and double click.

##### requirements.txt
The requirements.txt file should list all Python libraries that your notebooks depend on, and they will be installed using:

pip3 install -r requirements.txt

The code is tested with python3

##### How to use:

start a screen where the HttpServer will run.

**$screen -d -R HttpServer**

(Note this could instead be a systemd process started with systemctl or a e.g. docker container running nginx)
in screen do:

**$python3 HttpServer.py --filename ReceivedStatusInfo.log**

leave the screen with ctrl-A + ctrl-D

Start the Eventhandler with

**$python3 Eventhandler.py --bounce 30 --doubleclick 500 --timeout 60**

Timeout status events will occur one a minute and a button mounted as button 2 on the rpi GPIO pins will be detected
See chapter 2.5 in this reference https://gpiozero.readthedocs.io/en/stable/recipes.html where to mount the button






