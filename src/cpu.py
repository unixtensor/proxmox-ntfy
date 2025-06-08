import subprocess
import time
import math
import re

from print_t import print_t
from typing  import Optional
from ntfy    import Ntfy

last_cpu_check_warning: float = time.time()

class Tempature:
	warning_message: str = "🌡️ CPU is at a high tempature."
	timeout_check:   int = 180 # Seconds

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

	def __timeout_expired(self, last_check: float) -> bool:
		return (time.time() - last_check) > Tempature.timeout_check * 1000

	def ntfy_check(self):
		cpu_temp = self.get()
		if cpu_temp:
			cpu_temp = math.floor(cpu_temp)
			if cpu_temp >= self.warning_temp and self.__timeout_expired(last_cpu_check_warning):
				self.ntfy.send(f"{Tempature.warning_message} {cpu_temp} C")
		else:
			print_t("\033[31mCannot get a feasible tempature value for the CPU. (lm-sensors)\033[0m")
