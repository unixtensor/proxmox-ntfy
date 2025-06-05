import argparse
import time

import package
import cpu

from typing import Optional

clock_interval_secs: int = 1
last_check_debounce: int = 60 # Seconds
cpu_critical_temp:   int = 80
cpu_warning_temp:    int = 70

ntfy_url: Optional[str] = None
_ntfy_configure_prompt = """Please configure an ntfy url before starting.
\033[4mExamples:\033[0m
\033[32mpython3 main.py --url=10.0.13.37:42069
python3 main.py --url=ntfy.domain.com\033[0m"""

def cli_interface() -> bool:
	...

def start():
	print(f"Working! {time.time()}")
	while True:
		cpu.temperature_check()
		time.sleep(clock_interval_secs)

if __name__ == "__main__":
	if package.installed_list(["lm-sensors", "ntfy", "curl"]):
		if cli_interface():
			start()
		else:
			print(_ntfy_configure_prompt)