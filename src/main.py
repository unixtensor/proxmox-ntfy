import subprocess
import time
import re

from typing import Optional

clock_interval_secs: int   = 1
last_check_debounce: int   = 60 # Seconds
cpu_critical_temp:   int   = 80
cpu_warning_temp:    int   = 70
last_check:          float = time.time()
ntfy_url:            str   = "10.0.0.69"

def package_installed(package_name: str) -> Optional[bool]:
	try:
		installed = subprocess.run(["dpkg", "-s", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
		if not installed:
			print(f"Package \"{package_name}\" not installed.")
		return installed
	except Exception as err:
		print(err)
		return None

def packages_installed(package_list: list[str]) -> bool:
	for pkg_name in package_list:
		if not package_installed(pkg_name):
			return False
	return True

def cpu_temperature() -> Optional[float]:
	sensors_out = subprocess.check_output(["sensors"]).decode()
	for line in sensors_out.splitlines():
		if "Tctl" in line:
			match = re.search(r"(\d+\.\d+)°C", line)
			if match:
				return float(match.group(1))
	return None

def ntfy_send(message: str):
	try:
		global last_check
		last_check = time.time()
		subprocess.run(["curl", "-d", f"\"{message}\"", ntfy_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except Exception as err:
		print(f"Ntfy failed. {err}")

def clock_check_cpu():
	cpu_temp = cpu_temperature()
	if cpu_temp and (time.time() - last_check) > last_check_debounce * 1000:
		if cpu_temp >= cpu_critical_temp:
			ntfy_send(f"🔥 CPU tempature is at critical tempatures! {cpu_temp}")
		elif cpu_temp >= cpu_warning_temp:
			ntfy_send(f"🌡️ CPU tempature is at a high tempature. {cpu_temp}")

if packages_installed(["lm-sensors", "ntfy", "curl"]):
	print(f"Working! {time.time()}")
	while True:
		clock_check_cpu()
		time.sleep(clock_interval_secs)