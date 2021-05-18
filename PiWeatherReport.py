import time
from datetime import datetime

#for OLED
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image

import os
import sys

from time import sleep

#for WebAPI
import weatherapi

#for OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)	# 128x64

#for ImageFont
import imagefont
ttf = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font10 = None
font32 = None

basedir = os.path.dirname(os.path.realpath(__file__))
icondir = os.path.join(basedir, 'icons')

def get_display_item( data, index ):
	return ( datetime.fromtimestamp(data["hourly"][index]["dt"]),
			data["hourly"][index]["temp"],
			data["hourly"][index]["humidity"],
			data["hourly"][index]["weather"][0]["icon"] )

def display_item( draw, item ):
	icon_pixel = int( device.height * 0.7 )
	x = 0

	draw.text((x + 6, 0), item[0].strftime( "%H:%M"), font=font10, fill="white")

	logo = Image.open(os.path.join(icondir,  item[3][0:2] + ".bmp"))
	logo_resize = logo.resize((icon_pixel, icon_pixel))
	draw.bitmap((x + 6,6), logo_resize, fill='white')

	draw.text((x + 6, 52), str(int(item[1])) + "°C" + " / " + str(int(item[2])) + "%", font=font10, fill="white")

def display_clock( draw, timestamp ):
	x = device.width / 2
	time_datetime = datetime.fromtimestamp(timestamp)

	draw.text((x + 12,  0), time_datetime.strftime( "%H"), font=font32, fill="white")
	draw.text((x + 12, 30), time_datetime.strftime( "%M"), font=font32, fill="white")

def display_screen( item, time ):
	with canvas(device) as draw:
		display_item( draw, item )
		display_clock( draw, time )

def display( data ):
	currentUNIXTime = time.time()
	for i in range( len(data["hourly"]) ):
		#skip older items from current time
		if toHourUNIXTime( currentUNIXTime ) < data["hourly"][i]["dt"]:
			continue

		#Current hour + 3
		item = get_display_item( data, i+3 )
		break

	time_curr = int(time.time())
	time_prev = time_curr
	display_screen( item, time_curr )
	while (time_curr % 3600) != 0:
		time_curr = int(time.time())
		if (time_curr % 60 == 0) and (time_prev % 60 != 0):
			display_screen( item, time_curr )
		time_prev = time_curr
		time.sleep(0.25)

def toHourUNIXTime( UNIXTime ):
	hourSec  = 60 * 60
	return int( UNIXTime / hourSec ) * hourSec

def getNextHourUNIXTime( UNIXTime ):
	hourSec  = 60 * 60
	currHour = int( UNIXTime / hourSec ) * hourSec
	nextHour = currHour + hourSec

	return nextHour

def main():
	response = weatherapi.weatherapi()
	global font10
	font10 = imagefont.imagefont.font(ttf, 10)
	if font10 == None:
		sys.exit("** Err Not found : %s" % ttf)
	global font32
	font32 = imagefont.imagefont.font(ttf, 32)
	if font32 == None:
		sys.exit("** Err Not found : %s" % ttf)
	while True:
		api_data = response.get(True)
		if response.status_code() != 200:
			sys.exit("** Err Response : %d" % response.status_code())

		display( api_data )

if __name__ == '__main__':
	main()
