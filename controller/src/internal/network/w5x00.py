
import asyncio
import board
import busio
import digitalio
import supervisor
import time
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K, _DEFAULT_MAC 
from adafruit_wiznet5k.adafruit_wiznet5k_dhcp import DHCP
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
from internal.network.base import NetworkController

class W5x00:
    @staticmethod
    def reset():
        W5x00_RSTn = board.GP20
        ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
        ethernetRst.switch_to_output()
        ethernetRst.value = False
        time.sleep(0.1)
        ethernetRst.value = True
        return ethernetRst
    
    @staticmethod
    def SPIO():
        SPI0_SCK = board.GP18
        SPI0_TX = board.GP19
        SPI0_RX = board.GP16
        SPI0_CSn = board.GP17
        cs = digitalio.DigitalInOut(SPI0_CSn)
        spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)
        return spi_bus, cs

class W5x00Controller(NetworkController):
    def __init__(self):
        reset = W5x00.reset()
        spi_bus, cs = W5x00.SPIO()
        self.ethernet = WIZNET5K(spi_bus, cs, is_dhcp=False, debug=False)
        self.start_supervisor()

    @property
    def socket(self) -> tuple:
        return socket, self.ethernet

    @property
    def link_status(self) -> bool:
        return self.ethernet.link_status

    def connect(self, ifconfig: tuple, mac_address: bytes=_DEFAULT_MAC):
        try:
            self.dhcp = DHCP(self.ethernet, mac_address)
            self.dhcp.request_dhcp_lease()
            print("DHCP request successful.")
        except:
            self.ethernet.ifconfig = ifconfig
            print("DHCP failed. Using static IP.")

        print("Chip Version:", self.ethernet.chip)
        print("MAC Address:", WIZNET5K.pretty_mac(self.ethernet.mac_address))
        print("IP Address:", WIZNET5K.pretty_ip(self.ethernet.ip_address))
        print([WIZNET5K.pretty_ip(i) for i in self.ethernet.ifconfig])
        print("Connection successfully established!\n")
    
    async def supervisor(self):
        while True:
            if not self.link_status:
                print("Ethernet disconnected!")
                supervisor.reload()
            await asyncio.sleep(0.5)
