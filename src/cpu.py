import subprocess
import main
import ntfy
import time
import re

from typing import Optional

last_cpu_check: float = time.time()

def temperature() -> Optional[float]:
	sensors_out = subprocess.check_output(["sensors"]).decode()
	for line in sensors_out.splitlines():
		if "Tctl" in line:
			match = re.search(r"(\d+\.\d+)°C", line)
			if match:
				return float(match.group(1))
	return None

def temperature_check():
	cpu_temp = temperature()
	if cpu_temp and (time.time() - last_cpu_check) > main.last_check_debounce * 1000:
		if cpu_temp >= main.cpu_critical_temp:
			ntfy.send(f"🔥 CPU tempature is at critical tempatures! {cpu_temp}")
		elif cpu_temp >= main.cpu_warning_temp:
			ntfy.send(f"🌡️ CPU tempature is at a high tempature. {cpu_temp}")