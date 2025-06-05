import subprocess
import main
import time

last_ntfy_send: float = time.time()

def send(message: str):
	try:
		if main.ntfy_url:
			global last_ntfy_send
			last_ntfy_send = time.time()
			subprocess.run(["curl", "-d", f"\"{message}\"", main.ntfy_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			print("Ntfy send: url is not configured.")
	except Exception as err:
		print(f"Ntfy failed. {err}")