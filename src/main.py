import subprocess
import time
import re

from typing import Optional

clock_interval_secs = 1
last_check        = time.time()
cpu_critical_temp = 80
cpu_warning_temp  = 70

def package_installed(package_name: str) -> Optional[bool]:
	try:
		installed = subprocess.run(["pacman", "-Q", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
		if not installed:
			print(f"Package \"{package_name}\" not installed.")
		return installed
	except Exception as err:
		print(err)
		return None

def cpu_temperature() -> Optional[float]:
	sensors_out = subprocess.check_output(["sensors"]).decode()
	for line in sensors_out.splitlines():
		if "Tctl" in line:
			match = re.search(r"(\d+\.\d+)°C", line)
			if match:
				return float(match.group(1))
	return None

def clock_check_cpu():
	cpu_temp = cpu_temperature()
	if cpu_temp and (time.time() - last_check) > 1000:
		if cpu_temp >= cpu_critical_temp:
			print("")
		elif cpu_temp >= cpu_warning_temp:
			print("")

if package_installed("lm_sensors") and package_installed("ntfy"):
	while True:
		clock_check_cpu()
		time.sleep(clock_interval_secs)