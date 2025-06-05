import subprocess
import time
import re

from typing import Optional
from ntfy import Ntfy

last_cpu_check_unix: float = time.time()
last_cpu_check:      int   = 60 # Seconds

class Tempature:
	cpu_temp_crtitical_message: str = "🔥 CPU tempature is at critical tempatures!"
	cpu_temp_warning_message:   str = "🌡️ CPU tempature is at a high tempature."

	def __init__(self, ntfy_instance: Ntfy, cpu_critical_temp: int, cpu_warning_temp: int):
		self.cpu_critical_temp = cpu_critical_temp
		self.cpu_warning_temp = cpu_warning_temp
		self.ntfy = ntfy_instance

	def get(self) -> Optional[float]:
		sensors_out = subprocess.check_output(["sensors"]).decode()
		for line in sensors_out.splitlines():
			if "Tctl" in line:
				match = re.search(r"(\d+\.\d+)°C", line)
				if match:
					return float(match.group(1))
		return None

	def ntfy_check(self):
		cpu_temp = self.get()
		if cpu_temp and (time.time() - last_cpu_check_unix) > last_cpu_check * 1000:
			if cpu_temp >= self.cpu_critical_temp:
				self.ntfy.send(f"{Tempature.cpu_temp_crtitical_message} {cpu_temp}")
			elif cpu_temp >= self.cpu_warning_temp:
				self.ntfy.send(f"{Tempature.cpu_temp_warning_message} {cpu_temp}")
