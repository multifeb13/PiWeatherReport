import requests

API_KEY = "03308fa5a441cb0ddf1bfe85099e014d"
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