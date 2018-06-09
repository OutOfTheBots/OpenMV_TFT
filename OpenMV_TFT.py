'''
Copyright (c) 2018 Out of the BOTS
MIT License (MIT) 
Author: Shane Gingell
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from machine import Pin
import time
from ustruct import pack
from micropython import const


class TFT():
  st7735 = const(1)
  ili9341 = const(2)
  _SWRESET = const(0x01) # Software Reset
  _SLPOUT = const(0x11) # Sleep Out
  _COLMOD = const(0x3A) # Colour Mode
  _DISPON = const(0x29) # Display On
  _MADCTL = const(0x36) # Memory Data Access
  _CASET = const(0x2A) # Column Address Set
  _RASET = const(0x2B) # Row Address set
  _RAMWR = const(0x2C) #write to screen memory

  def send_spi(self,data, is_data):
    self.dc.value(is_data) #set data/command pin
    self.cs.value(0)
    self.hspi.write(data)
    self.cs.value(1)

  def __init__(self, spi, TFT_type, cs='P3', dc='P9'):
    self.hspi = spi
    self.cs = Pin(cs, Pin.OUT)
    self.dc = Pin(dc, Pin.OUT)

    if TFT_type ==1:
      self.send_spi(bytearray([_SWRESET]), False) #software reset
      time.sleep(200)
      self.send_spi(bytearray([_SLPOUT]), False)  #sleep out
      time.sleep(200)
      self.send_spi(bytearray([_COLMOD]), False)  #set 16 bit colour
      self.send_spi(bytearray([0x05]),True)
      self.send_spi(bytearray([_DISPON]), False)  #display on
      self.send_spi(bytearray([_MADCTL]), False)  #set mode for writing to screen
      self.send_spi(bytearray([0b10110000]),True) #this was the mode that I used for my screen
      self.send_spi(bytearray([_CASET]),False)    #set x writng window
      self.send_spi(pack(">HH", 0, 159), True)   #to 0 to 159
      self.send_spi(bytearray([_RASET]),False)    #set y writing window
      self.send_spi(pack(">HH", 0, 127), True)   #to 0 to 12

    elif TFT_type == 2:
      for command, data in (
        (0xef, b'\x03\x80\x02'),
        (0xcf, b'\x00\xc1\x30'),
        (0xed, b'\x64\x03\x12\x81'),
        (0xe8, b'\x85\x00\x78'),
        (0xcb, b'\x39\x2c\x00\x34\x02'),
        (0xf7, b'\x20'),
        (0xea, b'\x00\x00'),
        (0xc0, b'\x23'),  # Power Control 1, VRH[5:0]
        (0xc1, b'\x10'),  # Power Control 2, SAP[2:0], BT[3:0]
        (0xc5, b'\x3e\x28'),  # VCM Control 1
        (0xc7, b'\x86'),  # VCM Control 2
        (0x36, b'\xF8'),  # Memory Access Control
        (0x3a, b'\x55'),  # Pixel Format
        (0xb1, b'\x00\x18'),  # FRMCTR1
        (0xb6, b'\x08\x82\x27'),  # Display Function Control
        (0xf2, b'\x00'),  # 3Gamma Function Disable
        (0x26, b'\x01'),  # Gamma Curve Selected
        (0xe0, b'\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00'), # Set Gamma
        (0xe1, b'\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f')):  # Set Gamma
        self.send_spi(bytearray([command]), False)
        self.send_spi(data, True)
      self.send_spi(bytearray([0x11]), False)
      time.sleep(10)
      self.send_spi(bytearray([0x29]), False)


  def set_window(self, x, y, width, height):
    x_end=x+width-1
    y_end=y+height-1
    self.send_spi(bytearray([_CASET]),False)  # set Column addr command
    self.send_spi(pack(">HH", x, x_end), True)  # x_end
    self.send_spi(bytearray([_RASET]),False)  # set Row addr command
    self.send_spi(pack(">HH", y, y_end), True)  # y_end

  def write_to_screen(self, data):
    self.send_spi(bytearray([_RAMWR]),False)  # set to write to RAM
    self.send_spi(data, True)                 # send data

