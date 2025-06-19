import psutil
import time

from typing  import Optional, Callable
from print_t import print_t
from ntfy    import Ntfy

_init_run_critical: bool  = True
_init_run_warning:  bool  = True
_time_now:          float = time.time()

last_cpu_check_warning:  float = _time_now
last_cpu_check_crticial: float = _time_now

timeout_expired: Callable[[float, int], bool] = lambda c, t: (time.time() - c) > t

class Tempature:
	timeout_check_critical: int = 600 # Seconds
	timeout_check_warn:     int = 3600 # Seconds
	critical_message:       str = "🔥 CPU is at a very high tempature."
	warning_message:        str = "🌡️ CPU is at a high tempature."
	thermal_critical_c:     int = 80
	thermal_warn_c:         int = 70

	def __init__(self, ntfy_instance: Ntfy, cpu_temp_zone: str, cpu_temp_zone_label: str):
		self.ntfy = ntfy_instance
		self.cpu_temp_zone = cpu_temp_zone
		self.cpu_temp_zone_label = cpu_temp_zone_label

	def get(self) -> Optional[float]:
		for entry in psutil.sensors_temperatures().get(self.cpu_temp_zone, []):
			if entry.label == self.cpu_temp_zone_label:
				return entry.current
		return None

	def ntfy_check(self):
		cpu_temp = self.get()
		if cpu_temp:
			global _init_run_warning
			global _init_run_critical
			global last_cpu_check_warning
			global last_cpu_check_crticial

			cpu_temp = int(cpu_temp)

			if cpu_temp >= Tempature.thermal_warn_c and (_init_run_warning or timeout_expired(last_cpu_check_warning, Tempature.timeout_check_warn)):
				_init_run_warning = False
				last_cpu_check_warning = time.time()
				self.ntfy.send(message=f"{cpu_temp} C", title=Tempature.warning_message)
			if cpu_temp >= Tempature.thermal_critical_c and (_init_run_critical or timeout_expired(last_cpu_check_crticial, Tempature.timeout_check_critical)):
				_init_run_critical = False
				last_cpu_check_crticial = time.time()
				self.ntfy.send(message=f"{cpu_temp} C", title=Tempature.critical_message)
		else:
			print_t(f"\033[31mCannot get a feasible tempature value for the CPU. cpu_temp_zone={self.cpu_temp_zone} cpu_temp_zone_label={self.cpu_temp_zone_label}\033[0m")
