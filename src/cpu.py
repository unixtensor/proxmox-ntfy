import subprocess
import time
import math
import re

from print_t import print_t
from typing  import Optional
from ntfy    import Ntfy

_time_now = time.time()
last_cpu_check_warning: float = _time_now
cpu_temp_queue_check:   int   = 120 # Seconds

class Tempature:
	cpu_temp_warning_message: str = "🌡️ CPU is at a high tempature."

	def __init__(self, ntfy_instance: Ntfy, cpu_warning_temp: int):
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

	def __queue_time(self, last_check: float) -> bool:
		return (time.time() - last_check) > cpu_temp_queue_check * 1000

	def ntfy_check(self):
		cpu_temp = self.get()
		if cpu_temp:
			cpu_temp = math.floor(cpu_temp)
			if cpu_temp >= self.cpu_warning_temp and self.__queue_time(last_cpu_check_warning):
				self.ntfy.send(f"{Tempature.cpu_temp_warning_message} {cpu_temp} C")
		else:
			print_t("\033[31mCannot get a feasible tempature value for the CPU. (lm-sensors)\033[0m")
