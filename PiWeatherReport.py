import schedule
import time
from datetime import datetime

#for OLED
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

import item
item_info = None
item_separator = None
item_line = None
item_clock = None

import sys

from time import sleep

#for WebAPI
import weatherapi
response = None

#for OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)	# 128x64

m_update_data = True
m_update_disp = True
def cbr_every_hour():
	global m_update_data
	global m_update_disp
	m_update_data = True
	m_update_disp = True

def cbr_every_minute():
	global m_update_disp
	m_update_disp = True

def display( data ):
	with canvas(device) as draw:
		"""
		#Current hour + 3
		item_info.display(draw, response.hourly(data, 3), 0, 0, device.width / 2, device.height)
		item_separator.display(draw)
		#Current hour + 6
		item_info.display(draw, response.hourly(data, 6), device.width / 2, 0, device.width / 2, device.height)
		"""
		#Current hour + 3
		item_info.display( draw, response.hourly(data, 3), 0, 0, device.width / 2, device.height)
		item_clock.display(draw, device.width / 2)
		#moon age
		moon_age = response.moon(data,0)[2]
		if moon_age > 1:
			moon_age = 1
		moon_age_length = int(device.height * moon_age)
		item_line.display(	draw,
							device.width - 1, device.height - moon_age_length,
							device.width - 1, device.height)
		#gauge for moon age
		#upper
		item_line.display(	draw,
							device.width - 3, 0,
							device.width,     0)
		#center
		item_line.display(	draw,
							device.width - 3, device.height / 2,
							device.width,     device.height / 2)
		#lower
		item_line.display(	draw,
							device.width - 3, device.height - 1,
							device.width,     device.height - 1)

def setup():
	global item_info
	item_info = item.info()
	if item_info.is_ready() == False:
		sys.exit(1)
	global item_separator
	item_separator = item.separator(0, 0, device.width, device.height)
	if item_separator.is_ready() == False:
		sys.exit(1)
	global item_line
	item_line = item.line()
	if item_line.is_ready() == False:
		sys.exit(1)
	global item_clock
	item_clock = item.clock()
	if item_clock.is_ready() == False:
		exit(1)
	global response
	response = weatherapi.weatherapi()
	schedule.every().hour.at(":00").do(cbr_every_hour)
	schedule.every().minute.at(":00").do(cbr_every_minute)

def loop():
	global m_update_data
	global m_update_disp
	while True:
		if m_update_data == True:
			m_update_data = False
			api_data = response.get()
			if response.status_code() != 200:
				sys.exit("** Err Response : %d" % response.status_code())
		if m_update_disp == True:
			m_update_disp = False
			display( api_data )

		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
	setup()
	loop()
