import requests

from datetime import datetime

def print_t(out: str):
	t = datetime.now()
	print(f"({t.strftime('%Y-%m-%d')})[{t.strftime('%H:%M:%S')}]: " + out)

class Ntfy:
	def __init__(self, server: str):
		self.server = server

	def send(self, message: str):
		print_t(message)
		try:
			requests.post(self.server, data=message)
		except Exception as err:
			print_t(f"Ntfy failed. \033[31m{err}\033[0m")
