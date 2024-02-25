# From: https://learn.adafruit.com/building-circuitpython/build-circuitpython

sudo apt install python3-full gcc-arm-none-eabi

git clone https://github.com/adafruit/circuitpython.git
cd circuitpython
git checkout 8.2.10

pip3 install --upgrade -r requirements-dev.txt --break-system-packages
pip3 install --upgrade -r requirements-doc.txt --break-system-packages

cd frozen/
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_hashlib
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_AdafruitIO
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_RSA
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_Wiznet5k
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_asyncio
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_binascii
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_Logging
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_Requests
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_Ticks
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_WSGI
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_HTTPServer
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_binascii
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_datetime
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_Logging
git submodule add https://github.com/adafruit/Adafruit_CircuitPython_IterTools
git submodule add https://github.com/jimbobbennett/CircuitPython_HMAC
git submodule add https://github.com/jimbobbennett/CircuitPython_Base64
git submodule add https://github.com/jimbobbennett/CircuitPython_Parse

cd ../
cd ports/raspberrypi/
make fetch-port-submodules

cd ../../
cd frozen/
cd Adafruit_CircuitPython_hashlib && git checkout 1.4.15 && cd ..
cd Adafruit_CircuitPython_AdafruitIO && git checkout 5.8.1 && cd ..
cd Adafruit_CircuitPython_MiniMQTT && git checkout 7.5.8 && cd ..
cd Adafruit_CircuitPython_RSA && git checkout 1.2.19 && cd ..
cd Adafruit_CircuitPython_Wiznet5k && git checkout 5.0.6 && cd ..
cd Adafruit_CircuitPython_asyncio && git checkout 1.3.0 && cd ..
cd Adafruit_CircuitPython_binascii && git checkout 2.0.3 && cd ..
cd Adafruit_CircuitPython_Logging && git checkout 5.2.5 && cd ..
cd Adafruit_CircuitPython_Requests && git checkout 2.0.5 && cd ..
cd Adafruit_CircuitPython_Ticks && git checkout 1.0.13 && cd ..
cd Adafruit_CircuitPython_WSGI && git checkout 2.0.2 && cd ..
cd Adafruit_CircuitPython_HTTPServer && git checkout 4.5.5 && cd ..
cd Adafruit_CircuitPython_binascii && git checkout 2.0.3 && cd ..
cd Adafruit_CircuitPython_datetime && git checkout 1.2.7 && cd ..
cd Adafruit_CircuitPython_Logging && git checkout 5.2.5 && cd ..
cd Adafruit_CircuitPython_IterTools && git checkout 2.0.7 && cd ..
cd CircuitPython_HMAC && git checkout 0.2.1 && cd ..
cd CircuitPython_Base64 && git checkout 0.3.1 && cd ..
cd CircuitPython_Parse && git checkout 0.4.0 && cd ..

cd ..
cd ports/raspberrypi/
nano boards/wiznet_w5500_evb_pico/mpconfigboard.mk
"""mpconfigboard.mk
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_hashlib
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_AdafruitIO
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_MiniMQTT
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_RSA
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Wiznet5k
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_asyncio
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_binascii
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Logging
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Requests
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Ticks
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_WSGI
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_HTTPServer
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_binascii
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_datetime
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Logging
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_IterTools
FROZEN_MPY_DIRS += $(TOP)/frozen/CircuitPython_HMAC
FROZEN_MPY_DIRS += $(TOP)/frozen/CircuitPython_Base64
FROZEN_MPY_DIRS += $(TOP)/frozen/CircuitPython_Parse
"""mpconfigboard.mk

make BOARD=wiznet_w5500_evb_pico
