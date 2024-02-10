# simple-remote-protocol
Simple and lightweight protocol designed to communicate with devices running circuit python.

## Server

The server is a microcontroller running CircuitPython. This proyect is designed to run on a raspberry pi pico with a Wiznet W5500 ethernet module. But it can be easily adapted to run on other microcontrollers since it uses the `socket` module to communicate with the client.

### Dependences

This project runs on [CircuitPython 8.2.9](https://circuitpython.org/), so you will need a board that supports it. The board used in this project is the [W5500-EVB-Pico](https://circuitpython.org/board/wiznet_w5500_evb_pico/). You will also need to install the following libraries in your board:

- [adafruit_bus_device](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice)
- [adafruit_hashlib](https://github.com/adafruit/Adafruit_CircuitPython_hashlib)
- [adafruit_io](https://github.com/adafruit/Adafruit_CircuitPython_AdafruitIO)
- [adafruit_minimqtt](https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT)
- [adafruit_rsa](https://github.com/adafruit/Adafruit_CircuitPython_RSA)
- [adafruit_wiznet5k](https://github.com/adafruit/Adafruit_CircuitPython_Wiznet5k)
- [asyncio](https://github.com/adafruit/Adafruit_CircuitPython_asyncio)
- [adafruit_binascii](https://github.com/adafruit/Adafruit_CircuitPython_binascii)
- [adafruit_logging](https://github.com/adafruit/Adafruit_CircuitPython_Logging)
- [adafruit_requests](https://github.com/adafruit/Adafruit_CircuitPython_Requests)
- [adafruit_ticks](https://github.com/adafruit/Adafruit_CircuitPython_Ticks)
- [circuitpython_hmac](https://github.com/jimbobbennett/CircuitPython_HMAC)

More details on [LIB.md](LIB.md)

Libraries used in this project are ram consuming, so you will need a board with at least 256KB of RAM. Consider using a custom build of CircuitPython with the libraries built-in as frozen modules to reduce the RAM usage.

## Client

You can use any computer to run the client. In this project, a Raspberry Pi 4 Model B is used as a client to communicate with the microcontroller. It sends requests to the microcontroller and receives responses from it.

### Dependences

This project runs on [Python 3.9+](https://www.python.org/), so you will need to install it in your computer. You will also need to install the following libraries:

- [cryptography](https://cryptography.io/en/latest/)
