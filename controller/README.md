## Microcontroller

The server runs in a microcontroller running CircuitPython. This proyect is designed to run on a raspberry pi pico with a Wiznet W5500 ethernet module. But it can be easily adapted to run on other microcontrollers since it uses the `socket` module to communicate with the client.

### CircuitPython 8.2.10

This projects includes a custom build of CircuitPython 8.2.10 with all the libraries used in this project and a few others as frozen modules. This reduces the RAM usage and makes it possible to run the project on a Raspberry Pi Pico. You can find the custom build in the `uf2` folder.

### How to use

To use this project, after flashing the custom build of CircuitPython to your board, you will need to copy the `controller/src` folder to the root of the board. You will also need to create your own `config.json` with the network configuration to be used by the microcontroller. You can use one of the `config.json` files in the folder as a reference.

```python

### Dependences

This project runs on [CircuitPython 8.2.10](https://circuitpython.org/), so you will need a board that supports it. The board used in this project is the [W5500-EVB-Pico](https://circuitpython.org/board/wiznet_w5500_evb_pico/). You will also need to install the following libraries in your board:

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

More details on [LIBS.md](LIBS.md)

Libraries used in this project are ram consuming, so you will need a board with at least 256KB of RAM. Consider using a custom build of CircuitPython with the libraries built-in as frozen modules to reduce the RAM usage.

### Custom Build

This project includes a custom build of CircuitPython 8.2.10 with all the libraries used in this project and a few others as frozen modules. You can flash the custom build to your board using the `frozenlibs-circuitpython-w5500_evb_pico-8.2.10.uf2` file in the `uf2` folder. This build is designed to run only on the W5500-EVB-Pico board.

If you want to build your own custom build of CircuitPython with other libraries or for other boards, you can use the `frozenlibs-build.sh` file in the `uf2` folder as a reference. This command is not prepared to be run as is, you will need to modify it to fit your needs.
