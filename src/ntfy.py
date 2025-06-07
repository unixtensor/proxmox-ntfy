import requests
import time

from datetime import datetime

class Ntfy:
	def __init__(self, server: str):
		self.server = server

	def send(self, message: str):
		try:
			pretty_date_time = datetime.fromtimestamp(time.time())
			print(f"[{pretty_date_time}]: {message}")
			requests.post(self.server, data=message)
		except Exception as err:
			print(f"Ntfy failed. {err}")
