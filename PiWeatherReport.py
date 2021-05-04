#https://qiita.com/optimisuke/items/87d4846de15736b599e4

import requests
import json
import time
from datetime import datetime

#for OLED
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageChops

import os

from time import sleep

API_KEY = "03308fa5a441cb0ddf1bfe85099e014d"
api = "https://api.openweathermap.org/data/2.5/onecall?lat=35.681236&lon=139.767125&units=metric&lang=ja&appid={key}"

#for OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)	# 128x64

ttf = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font10 = ImageFont.truetype(ttf, 10)

basedir = os.path.dirname(os.path.realpath(__file__))
icondir = os.path.join(basedir, 'icons')

def getResponse():
	url = api.format(key = API_KEY)
	#print(url)

	return requests.get(url)

def toJson( response ):
	return json.loads( response.text )

def display( item_left, item_right ):
	icon_pixel = int( device.height * 0.7 )

	with canvas(device) as draw:
		for i in range( 0, 2 ):
			if i == 0:
				item = item_left
				x = 0
			else:
				item = item_right
				x = device.width / 2

			draw.text((x + 6, 0), item[0].strftime( "%H:%M"), font=font10, fill="white")

			logo = Image.open(os.path.join(icondir,  item[3][0:2] + ".bmp"))
			logo_resize = logo.resize((icon_pixel, icon_pixel))
			draw.bitmap((x,6), logo_resize, fill='white')

			draw.text((x + 6, 52), str(int(item[1])) + "°C" + " / " + str(int(item[2])) + "%", font=font10, fill="white")

		draw.line( (x, 2, x, device.height - 2), fill="white", width=1 )

def toHourUNIXTime( UNIXTime ):
	hourSec  = 60 * 60
	return int( UNIXTime / hourSec ) * hourSec

def getNextHourUNIXTime( UNIXTime ):
	hourSec  = 60 * 60
	currHour = int( UNIXTime / hourSec ) * hourSec
	nextHour = currHour + hourSec

	return nextHour

def main():
	while True:
		response = getResponse()
		data = toJson( response )

		currentUNIXTime = time.time()
		for i in range( len(data["hourly"]) ):
			#skip older items from current time
			if toHourUNIXTime( currentUNIXTime ) < data["hourly"][i]["dt"]:
				continue

			#Current hour + 3
			item_left = ( datetime.fromtimestamp(data["hourly"][i + 3]["dt"]),
						data["hourly"][i + 3]["temp"],
						data["hourly"][i + 3]["humidity"],
						data["hourly"][i + 3]["weather"][0]["icon"] )
			#Current hour + 6
			item_right = ( datetime.fromtimestamp(data["hourly"][i + 6]["dt"]),
						data["hourly"][i + 6]["temp"],
						data["hourly"][i + 6]["humidity"],
						data["hourly"][i + 6]["weather"][0]["icon"] )
			display( item_left, item_right )
			break

		timeCurrentUNIXTime = time.time()
		sleep( getNextHourUNIXTime( timeCurrentUNIXTime ) - timeCurrentUNIXTime )

if __name__ == '__main__':
	main()
