import subprocess
import time
import math
import re

from print_t import print_t
from typing  import Optional
from ntfy    import Ntfy

_time_now = time.time()

last_cpu_check_warning: float = _time_now
last_cpu_warning_set:   float = _time_now
last_warning_temp:      int   = 0

def timeout_expired(check: float, timeout: int) -> bool:
	return (time.time() - check) > timeout * 1000

class Tempature:
	warning_message: str = "🌡️ CPU is at a high tempature."
	timeout_check:   int = 60 # Seconds

	def __init__(self, ntfy_instance: Ntfy, warning_temp: int):
		self.warning_temp = warning_temp
		self.ntfy = ntfy_instance

	def get(self) -> Optional[float]:
		sensors_out = subprocess.check_output(["sensors"]).decode()
		for line in sensors_out.splitlines():
			if "Tctl" in line:
				match = re.search(r"(\d+\.\d+)°C", line)
				if match:
					return float(match.group(1))
		return None

	def __warn(self, cpu_temp: int):
		pad = 0
		if timeout_expired(last_cpu_warning_set, Tempature.timeout_check * 5):
			#If the timeout expired, send a notify immediately
			global last_warning_temp
			last_warning_temp = 0
		else:
			#If the timeout is still active, apply padding to the current CPU tempature so its less spammy
			pad = 5
		if cpu_temp + pad > last_warning_temp:
			message = f"{cpu_temp} C."
			if last_warning_temp != 0:
				message += f" The tempature has risen by: {cpu_temp - last_warning_temp} C. 📈"
			last_warning_temp = cpu_temp
			self.ntfy.send(message=message, title=Tempature.warning_message)

	def ntfy_check(self):
		cpu_temp = self.get()
		if cpu_temp:
			cpu_temp = math.floor(cpu_temp)
			if cpu_temp >= self.warning_temp and timeout_expired(last_cpu_check_warning, Tempature.timeout_check):
				self.__warn(cpu_temp)
		else:
			print_t("\033[31mCannot get a feasible tempature value for the CPU. (lm-sensors)\033[0m")
