import requests
import json
from datetime import datetime

API_KEY = "{API_KEY}"
EXCLUDE= "current,minutely"
api = "https://api.openweathermap.org/data/2.5/onecall?lat=35.681236&lon=139.767125&units=metric&lang=ja&exclude={exclude}&appid={key}"

m_status_code = 0

class weatherapi:
	def __init__(self):
		pass

	def get(self):
		url = api.format(exclude = EXCLUDE, key = API_KEY)
		#print(url)

		request = requests.get(url)
		global m_status_code
		m_status_code = request.status_code
		#print(m_status_code)

		return json.loads( request.text )

	def hourly(self, data, index):
		return ( datetime.fromtimestamp(data["hourly"][index]["dt"]),
				data["hourly"][index]["temp"],
				data["hourly"][index]["humidity"],
				data["hourly"][index]["weather"][0]["icon"] )

	def moon(self, data, index):
		return (
				datetime.fromtimestamp(data["daily"][index]["moonrise"]),
				datetime.fromtimestamp(data["daily"][index]["moonset"]),
				data["daily"][index]["moon_phase"],
				)

	def status_code(self):
		return m_status_code

if __name__ == '__name__':
	pass