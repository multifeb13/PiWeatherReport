from PIL import ImageFont
import os

class imagefont:
	def __init__(self):
		pass

	def font(file, size):
		if os.path.exists(file):
			#print(file)
			return ImageFont.truetype(file, size)
		else:
			return None

if __name__ == '__main__':
	pass