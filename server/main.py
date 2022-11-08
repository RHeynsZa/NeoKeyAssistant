import time
import serial


# index,hexcode,mode,brightness
# command = b"0,EE0022,blink,50\n\r"

ser = serial.Serial("/dev/ttyACM1", 115200)  # open serial port

num_pixels = 4

for i in range(num_pixels):
    ser.write(bytes(f"{i},FF0000,blink\n\r", "utf-8"))
    time.sleep(2)
    ser.write(bytes(f"{i},00FF00,blink\n\r", "utf-8"))
    time.sleep(2)
    ser.write(bytes(f"{i},0000FF,blink\n\r", "utf-8"))
    time.sleep(2)
    ser.write(bytes(f"{i},000000,solid\n\r", "utf-8"))


ser.close()
