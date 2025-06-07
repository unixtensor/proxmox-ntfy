import requests
import time

from datetime import datetime

class Ntfy:
	def __init__(self, server: str):
		self.server = server

	def send(self, message: str):
		print(f"[{datetime.fromtimestamp(time.time())}]: {message}")
		try:
			requests.post(self.server, data=message)
		except Exception as err:
			print(f"Ntfy failed. {err}")
