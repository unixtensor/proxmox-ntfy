import requests

class Ntfy:
	def __init__(self, server: str):
		self.server = server

	def send(self, message: str):
		try:
			requests.post(self.server, data=message)
		except Exception as err:
			print(f"Ntfy failed. {err}")
