import requests
import json

API_KEY = "{API_KEY}"
api = "https://api.openweathermap.org/data/2.5/onecall?lat=35.681236&lon=139.767125&units=metric&lang=ja&appid={key}"

m_status_code = 0

class weatherapi:
	def __init__(self):
		pass

	def get(self, mode_json=False):
		url = api.format(key = API_KEY)
		#print(url)

		request = requests.get(url)
		global m_status_code
		m_status_code = request.status_code
		#print(m_status_code)

		if mode_json == True:
			return json.loads( request.text )
		return request

	def status_code(self):
		return m_status_code

if __name__ == '__name__':
	pass