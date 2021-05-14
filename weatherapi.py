import requests

API_KEY = "{API_KEY}"
api = "https://api.openweathermap.org/data/2.5/onecall?lat=35.681236&lon=139.767125&units=metric&lang=ja&appid={key}"

class weatherapi:
	def __init__(self):
		pass

	def get(self):
		url = api.format(key = API_KEY)
		#print(url)

		return requests.get(url)

if __name__ == '__name__':
	pass