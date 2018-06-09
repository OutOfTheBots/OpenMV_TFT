#TFT screen demo to steam frame buffer to a external SPI screen

import sensor, image, time
from machine import SPI
from OpenMV_TFT import TFT

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

spi = SPI(2, baudrate=54000000) #create an SPI bus

#create an instance of the screen driver
#you mustr pass a SPI bus and type of screen (ili9341 or st7735
#optional can pass cs pin and dc pin default is cs='P3' and dc='P9'
screen = TFT(spi, TFT.st7735)

#set window on screen to write to (x_start, Y_start, width, height)
#the window needs to be inside the resolution of the screen and must match the exact size of fb
screen.set_window(0,0,160,120)


while(True):
    clock.tick()
    img = sensor.snapshot()

    # some image processing code goes here...

    screen.write_to_screen(img) #send the fb to the screen
    print(clock.fps())
