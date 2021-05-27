import schedule
import time
from datetime import datetime

#for OLED
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

import screen
_screen = None
_screen_mode = 2

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

def setup():
	global response
	response = weatherapi.weatherapi()
	global _screen
	if _screen_mode == 1:
		schedule.every().hour.at(":00").do(cbr_every_hour)
		_screen = screen.screen_2items(device)
	else:
		schedule.every().hour.at(":00").do(cbr_every_hour)
		schedule.every().minute.at(":00").do(cbr_every_minute)
		_screen = screen.screen_item_with_clock(device)

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
			with canvas(device) as draw:
				_screen.display(draw, api_data)

		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
	setup()
	loop()
