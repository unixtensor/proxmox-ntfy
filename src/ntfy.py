import requests

from print_t import print_t

class Ntfy:
	def __init__(self, server: str, logging_disabled: bool):
		self.server = server
		self.logging_disabled = logging_disabled

	def send(self, message: str):
		if not self.logging_disabled:
			print_t("Ntfy OUT: " + message)
		try:
			requests.post(self.server, data=message.encode(encoding="utf-8"))
		except Exception as err:
			print_t(f"\033[31m{err}\033[0m")
