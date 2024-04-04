import board
import busio
import digitalio
import time
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K, _DEFAULT_MAC
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
        time.sleep(1)
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
    def __init__(self, mac_address: bytes=_DEFAULT_MAC, debug: bool=False):
        reset = W5x00.reset()
        spi_bus, cs = W5x00.SPIO()
        self.ethernet = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=mac_address, debug=debug)
    
    def connect(self, ifconfig: tuple, mac_address: bytes=_DEFAULT_MAC, is_dhcp: bool=True):
        self.ethernet.mac_address = mac_address
        if is_dhcp:
            try:
                self.ethernet.set_dhcp()
            except RuntimeError as e:
                self.ethernet.ifconfig = ifconfig
                print("DHCP failed. Using static IP.")
        else:
            self.ethernet.ifconfig = ifconfig
        print("Connection successfully established!\n")

    @property
    def link_status(self) -> bool:
        return self.ethernet.link_status
    
    @property
    def socket(self):
        socket.set_interface(self.ethernet)
        return socket
    
    @property
    def interface(self):
        return self.ethernet

    def debug_info(self):
        print("Chip Version:", self.ethernet.chip)
        print("MAC Address:", WIZNET5K.pretty_mac(self.ethernet.mac_address))
        ifconfig = (WIZNET5K.pretty_ip(ip) for ip in self.ethernet.ifconfig)
        print("IP Address:  {}\nSubnet Mask: {}\nGW Address:  {}\nDNS Server:  {}".format(*ifconfig))
