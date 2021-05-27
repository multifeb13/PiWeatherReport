import item
import weatherapi

class screen():
	def __init__(self, device):
		self.device = device

		self.item_info = item.info()
		if self.item_info.is_ready() == False:
			sys.exit(1)
		self.item_separator = item.separator(0, 0, device.width, device.height)
		if self.item_separator.is_ready() == False:
			sys.exit(1)
		self.item_line = item.line()
		if self.item_line.is_ready() == False:
			sys.exit(1)
		self.item_clock = item.clock()
		if self.item_clock.is_ready() == False:
			exit(1)

		self.response=weatherapi.weatherapi()

		self.is_ready = False

class screen_2items(screen):
	def __init__(self, device):
		super().__init__(device)

	def display(self, draw, data, left=3, right=6):
		#2 items
		width_half = self.device.width / 2
		hour = (left, right)
		for i in range(2):
			self.item_info.display(
				draw,
				self.response.hourly(data, hour[i]),	#current hour + alpha
				width_half * i,	0,
				width_half,		self.device.height)
		#separator
		self.item_separator.display(draw)

class screen_item_with_clock(screen):
	def __init__(self, device):
		super().__init__(device)

	def display(self, draw, data):
		#Current hour + 3
		self.item_info.display( draw, self.response.hourly(data, 3), 0, 0, self.device.width / 2, self.device.height)
		self.item_clock.display(draw, self.device.width / 2)
		#moon age
		moon_age = self.response.moon(data,0)[2]
		if moon_age > 1:
			moon_age = 1
		moon_age_length = int(self.device.height * moon_age)
		self.item_line.display(	draw,
							self.device.width - 1, self.device.height - moon_age_length,
							self.device.width - 1, self.device.height)
		#gauge for moon age
		#new moon
		gauge_x = self.device.width
		gauge_step = 4	#4 steps, 5 lines
		for i in range(gauge_step + 1):
			gauge_y = self.device.height / gauge_step * i
			if gauge_y >= self.device.height:
				gauge_y = self.device.height - 1
			self.item_line.display(	draw,
									gauge_x - 3,	gauge_y,
									gauge_x, 		gauge_y)
