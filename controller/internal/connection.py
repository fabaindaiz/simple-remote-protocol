import asyncio
import board
import busio
import digitalio
import supervisor
import time
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
from microcontroller import watchdog
from watchdog import WatchDogMode

from internal.config import MY_MAC, IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER


class WiznetConnection:
        
    def __init__(self):
        self.ethernet = None
        self.reset = False

        ##SPI0
        SPI0_SCK = board.GP18
        SPI0_TX = board.GP19
        SPI0_RX = board.GP16
        SPI0_CSn = board.GP17

        ##reset
        W5x00_RSTn = board.GP20

        ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
        ethernetRst.direction = digitalio.Direction.OUTPUT

        # For Adafruit Ethernet FeatherWing
        self.cs = digitalio.DigitalInOut(SPI0_CSn)

        # cs = digitalio.DigitalInOut(board.D5)
        self.spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

        # Reset W5500 first
        ethernetRst.value = False
        time.sleep(1)
        ethernetRst.value = True

    def connect(self):
        # Initialize ethernet interface
        self.ethernet = WIZNET5K(self.spi_bus, self.cs, is_dhcp=False, mac=MY_MAC, debug=False)
        
        self.ethernet.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

        print("Chip Version:", self.ethernet.chip)
        print("MAC Address:", [hex(i) for i in self.ethernet.mac_address])
        print("My IP address is:", self.ethernet.pretty_ip(self.ethernet.ip_address))

        if not self.ethernet.link_status:
            print("Ethernet disconnected!")
            supervisor.reload()

        print("Connection successfully established!\n")

    async def supervisor(self):
        #watchdog.timeout = 5
        #watchdog.mode = WatchDogMode.RESET

        while True:
            if not self.ethernet.link_status or self.reset:
                print("Ethernet disconnected!")
                supervisor.reload()

            #watchdog.feed()
            await asyncio.sleep(1)
