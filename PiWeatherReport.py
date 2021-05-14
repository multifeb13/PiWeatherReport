import json
import time
from datetime import datetime

#for OLED
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageChops

import os

from time import sleep

#for WebAPI
import weatherapi

#for OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)	# 128x64

ttf = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font10 = ImageFont.truetype(ttf, 10)

basedir = os.path.dirname(os.path.realpath(__file__))
icondir = os.path.join(basedir, 'icons')

def toJson( response ):
	return json.loads( response.text )

def get_display_item( data, index ):
	return ( datetime.fromtimestamp(data["hourly"][index]["dt"]),
			data["hourly"][index]["temp"],
			data["hourly"][index]["humidity"],
			data["hourly"][index]["weather"][0]["icon"] )

def display_item( draw, item, index_lr ):
	icon_pixel = int( device.height * 0.7 )
	if index_lr == 0:
		x = 0
	else:
		x = device.width / 2

	draw.text((x + 6, 0), item[0].strftime( "%H:%M"), font=font10, fill="white")

	logo = Image.open(os.path.join(icondir,  item[3][0:2] + ".bmp"))
	logo_resize = logo.resize((icon_pixel, icon_pixel))
	draw.bitmap((x + 6,6), logo_resize, fill='white')

	draw.text((x + 6, 52), str(int(item[1])) + "°C" + " / " + str(int(item[2])) + "%", font=font10, fill="white")

def display_separator( draw ):
	x = device.width / 2
	draw.line( (x, 2, x, device.height - 2), fill="white", width=1 )

def display( data ):
	currentUNIXTime = time.time()
	for i in range( len(data["hourly"]) ):
		#skip older items from current time
		if toHourUNIXTime( currentUNIXTime ) < data["hourly"][i]["dt"]:
			continue

		#Current hour + 3
		item_left  = get_display_item( data, i+3 )
		#Current hour + 6
		item_right = get_display_item( data, i+6 )
		break

	with canvas(device) as draw:
		display_item( draw, item_left,  0 )
		display_item( draw, item_right, 1 )
		display_separator( draw )

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
	while True:
		data = toJson( response.get() )
		display( data )

		timeCurrentUNIXTime = time.time()
		sleep( getNextHourUNIXTime( timeCurrentUNIXTime ) - timeCurrentUNIXTime )

if __name__ == '__main__':
	main()
