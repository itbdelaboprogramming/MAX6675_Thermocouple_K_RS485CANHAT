import time
import spidev

# wiring
# Raspberry         MAX6675
#       GND   ------   GND
#        5V     ------   VCC
#   pin 18     ------   SCK
#   pin 22     ------   CS
#   pin 16     ------   SO

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 0

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 4300000


while 1:
    raw_data =spi.readbytes(2)
    int_data = (raw_data[0] << 8) | raw_data[1]
    bit_data = '{0:016b}'.format(int_data)
    
    # bit 1 = three-state (0)
    #bit 2 = 0 must be
    # bit 3 = 0 if connectd correctly
    # so if bit data (3-1) = 4 or 100 the break send error
    if(int_data & 0x4):
        print("Check wiring")
        break
    #since bit 14-3 is the data and 15 is always 0
    
    temp_data = (int_data >>3)
    temp_data = temp_data*0.25-2.5
    print(temp_data)
    time.sleep(1)
