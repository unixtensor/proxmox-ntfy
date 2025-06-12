import subprocess
import time
import math
import re

from print_t import print_t
from typing  import Optional
from ntfy    import Ntfy

_init_run_critical: bool  = True
_init_run_warning:  bool  = True
_time_now:          float = time.time()

last_cpu_check_warning:  float = _time_now
last_cpu_check_crticial: float = _time_now

def timeout_expired(check: float, timeout: int) -> bool:
	return (time.time() - check) > timeout

class Tempature:
	timeout_check_critical: int = 120 # Seconds
	timeout_check_warn:     int = 300 # Seconds
	critical_message:       str = "🔥 CPU is at a very high tempature."
	warning_message:        str = "🌡️ CPU is at a high tempature."
	thermal_critical_c:     int = 80
	thermal_warn_c:         int = 70

	def __init__(self, ntfy_instance: Ntfy):
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
		if cpu_temp:
			global _init_run_warning
			global _init_run_critical
			global last_cpu_check_warning
			global last_cpu_check_crticial

			cpu_temp = math.floor(cpu_temp)
			if cpu_temp >= Tempature.thermal_warn_c and (_init_run_warning or timeout_expired(last_cpu_check_warning, Tempature.timeout_check_warn)):
				_init_run_warning = False
				last_cpu_check_warning = time.time()
				self.ntfy.send(message=f"{cpu_temp} C", title=Tempature.warning_message)
			if cpu_temp >= Tempature.thermal_critical_c and (_init_run_critical or timeout_expired(last_cpu_check_crticial, Tempature.timeout_check_critical)):
				_init_run_critical = False
				last_cpu_check_crticial = time.time()
				self.ntfy.send(message=f"{cpu_temp} C", title=Tempature.critical_message)
		else:
			print_t("\033[31mCannot get a feasible tempature value for the CPU. (lm-sensors)\033[0m")
