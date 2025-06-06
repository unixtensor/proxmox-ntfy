import time
import sys

import package
import cli
import cpu

from ntfy import Ntfy

_ntfy_configure_prompt = """\033[4mPlease configure an ntfy url before starting.\033[0m
Examples:
\033[32mpython3 main.py 10.0.13.37:42069
python3 main.py ntfy.domain.com\033[0m"""

def start(
	cpu_critical_temp: int,
	cpu_warning_temp: int,
	ntfy_server: str,
	interval: int
):
	ntfy = Ntfy(ntfy_server)
	ntfy_cpu_temp_monitor = cpu.Tempature(ntfy, cpu_critical_temp, cpu_warning_temp)

	print(f"Started. {time.time()}")
	print("Ntfy monitoring software is now listening.")

	while True:
		ntfy_cpu_temp_monitor.ntfy_check()
		time.sleep(interval)

if __name__ == "__main__":
	if package.installed("lm-sensors"):
		if len(sys.argv) > 1:
			cli_args = cli.interface()
			start(
				cli_args.cpu_temp_critical,
				cli_args.cpu_temp_warning,
				sys.argv[1],
				cli_args.update_rate,
			)
		else:
			print(_ntfy_configure_prompt)