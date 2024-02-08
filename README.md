# simple-remote-protocol
Simple and lightweight protocol designed to communicate with devices running circuit python.

## Microcontroller

Microcontroller firmware is used to communicate with the computer. It receives requests from the computer and sends responses to it.

### Dependences

This project runs on [CircuitPython](https://circuitpython.org/), so you will need a board that supports it. The board used in this project is the [W5500-EVB-Pico](https://circuitpython.org/board/wiznet_w5500_evb_pico/).

Libraries used in this project are ram consuming, so you will need a board with at least 256KB of RAM. Consider using a custom build of CircuitPython with the libraries built-in as frozen modules to reduce the RAM usage.

You will also need to install the following libraries in your board, for more details see the LIB.md file:

- adafruit_bus_device
- adafruit_hashlib
- adafruit_io
- adafruit_minimqtt
- adafruit_rsa
- adafruit_wiznet5k
- asyncio
- adafruit_binascii
- adafruit_logging
- adafruit_requests
- adafruit_ticks
- circuitpython_hmac

## Computer

Computer is used as a client to communicate with the microcontroller. It sends requests to the microcontroller and receives responses from it.

### Dependences

This project runs on [Python 3.9+](https://www.python.org/), so you will need to install it in your computer. You will also need to install the following libraries:

- [python 3.9+](https://www.python.org/)
- [cryptography](https://cryptography.io/en/latest/)
