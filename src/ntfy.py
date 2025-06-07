import requests

from print_t import print_t

class Ntfy:
	def __init__(self, server: str):
		self.server = server

	def send(self, message: str):
		print_t("Ntfy OUT: " + message)
		try:
			requests.post(self.server, data=message)
		except Exception as err:
			print_t(f"\033[31m{err}\033[0m")
