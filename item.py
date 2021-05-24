import imagefont
import time
from datetime import datetime
import os
from PIL import Image

TTF = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

class item():
	def __init__(self):
		self.ready = False

	def is_ready(self):
		return self.ready

	def display(self, draw):
		pass

class info(item):
	def __init__(self, fontsize=10):
		super().__init__()

		self.fontsize = fontsize
		self.font = imagefont.imagefont.font(TTF, self.fontsize)
		if self.font == None:
			return

		basedir = os.path.dirname(os.path.realpath(__file__))
		self.icondir = os.path.join(basedir, 'icons')
		if os.path.exists(self.icondir) == False:
			return

		self.ready = True

	def display(self, draw, data, x, y, width, height):
		draw.text((x + 6, y + 0), data[0].strftime( "%H:%M"), font=self.font, fill="white")

		icon_pixel = int( height * 0.7 )
		logo = Image.open(os.path.join(self.icondir,  data[3][0:2] + ".bmp"))
		logo_resize = logo.resize((icon_pixel, icon_pixel))
		draw.bitmap((x + 6, y + 6), logo_resize, fill='white')

		draw.text((x + 6, y + 52), str(int(data[1])) + "°C" + " / " + str(int(data[2])) + "%", font=self.font, fill="white")

class separator(item):
	def __init__(self, x, y, device_width, device_height):
		super().__init__()
		self.x = x
		self.y = y
		self.device_width = device_width
		self.device_height = device_height
		self.center_x = self.device_width / 2
		self.center_y = self.device_height / 2
		self.mergin = 2
		self.ready = True

	def display(self, draw, vertical=True):
		if vertical == True:
			_x1 = self.center_x
			_y1 = self.y + self.mergin
			_x2 = _x1
			_y2 = self.device_height - self.mergin
		else:
			_x1 = self.x + self.mergin
			_y1 = self.center_y
			_x2 = self.device_width - self.mergin
			_y2 = self.center_y
		draw.line( (_x1, _y1, _x2, _y2), width=1, fill="white")

class line(item):
	def __init__(self):
		super().__init__()
		self.ready = True

	def display(self, draw, x1, y1, x2, y2):
		draw.line( (x1, y1, x2, y2), width=1, fill="white")

class clock(item):
	def __init__(self, fontsize=32):
		super().__init__()

		self.fontsize = fontsize
		self.font = imagefont.imagefont.font(TTF, self.fontsize)
		if self.font == None:
			return

		self.ready = True

	def display(self, draw, x=0, y=0, timestamp=None):
		if timestamp == None:
			timestamp = time.time()
		time_datetime = datetime.fromtimestamp(timestamp)

		draw.text((x + 12,  0), time_datetime.strftime( "%H"), font=self.font, fill="white")
		draw.text((x + 12, 30), time_datetime.strftime( "%M"), font=self.font, fill="white")
