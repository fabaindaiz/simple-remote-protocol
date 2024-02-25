# simple-remote-protocol
Simple and lightweight protocol designed to communicate with devices running circuit python.

## Server

The server is a microcontroller running CircuitPython. This proyect is designed to run on a raspberry pi pico with a Wiznet W5500 ethernet module. But it can be easily adapted to run on other microcontrollers since it uses the `socket` module to communicate with the client.

More details on [controller folder](controller/)

## Client

You can use any computer to run the client. In this project, a Raspberry Pi 4 Model B is used as a client to communicate with the microcontroller. It sends requests to the microcontroller and receives responses from it.

More details on [client folder](client/)

### Aknowledgements

- [Adafruit](https://www.adafruit.com/) for the libraries used in this project.
- [CircuitPython](https://circuitpython.org/) for the firmware used in this project.
- [Wiznet](https://www.wiznet.io/) for the W5500 ethernet module used in this project.

All licenses and attributions for the libraries and redistributable files used in this project can be found in the [licences folder](licences/).

This proyect has no relation with Adafruit, CircuitPython or Wiznet. It is an independent project made for learning purposes.
