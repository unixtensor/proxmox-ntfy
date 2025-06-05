import time

import package
import cli
import cpu

from ntfy import Ntfy

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
	if package.installed_list(["lm-sensors", "ntfy", "curl"]):
		cli_args = cli.interface()
		start(
			cli_args.cpu_temp_critical,
			cli_args.cpu_temp_warning,
			cli_args.server,
			cli_args.update_rate,
		)