import subprocess

class Ntfy:
	def __init__(self, server: str):
		self.server = server

	def send(self, message: str):
		try:
			subprocess.run(["curl", "-d", f"\"{message}\"", self.server], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except Exception as err:
			print(f"Ntfy failed. {err}")
