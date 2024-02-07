# simple-remote-protocol
Simple and lightweight protocol designed to communicate with devices running circuit python.

## Microcontroller

Microcontroller firmware is used to communicate with the computer. It receives requests from the computer and sends responses to it.

### Dependences

This project runs on [CircuitPython](https://circuitpython.org/), so you will need a board that supports it. The board used in this project is the [W5500-EVB-Pico](https://circuitpython.org/board/wiznet_w5500_evb_pico/).

You will also need to install the following libraries in your board:

#### Libraries included in the CircuitPython bundle
- [adafruit_bus_device]()
- [adafruit_hashlib]()
- [adafruit_httpserver]()
- [adafruit_io]()
- [adafruit_itertools]()
- [adafruit_minimqtt]()
- [adafruit_rsa]()
- [adafruit_wiznet5k]()
- [adafruit_wsgi]()
- [asyncio]()
- [adafruit_binascii]()
- [adafruit_dht]()
- [adafruit_logging]()
- [adafruit_requests]()
- [adafruit_ticks]()

#### Libraries not included in the CircuitPython bundle
- [circuitpython_hmac](https://github.com/jimbobbennett/CircuitPython_HMAC)

## Computer

Computer is used as a client to communicate with the microcontroller. It sends requests to the microcontroller and receives responses from it.

### Dependences

This project runs on [Python 3.9+](https://www.python.org/), so you will need to install it in your computer. You will also need to install the following libraries:

- [python 3.9+](https://www.python.org/)
- [cryptography](https://cryptography.io/en/latest/)
