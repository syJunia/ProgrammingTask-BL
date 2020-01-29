Initial version of a program solving the:

An application in python that runs on a raspberry pi that can detect events from a button connected to a GPIO pin and create a message in json format and send it to a “cloud server” using a REST interface and save the data in a file on the server. The application should also send status message at regular intervals to the server e.g. the current time.
For test: The server could be a local server that can receive the messages and save them in a file.

The button handling should handle contact bouncing and be able to detect different button events such as click, and double click.





