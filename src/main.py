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
	if package.installed("lm-sensors"):
		cli_args    = cli.Interface()
		parsed      = cli_args.parsed_args()
		ntfy_server = cli_args.argv_1()
		if ntfy_server:
			start(
				parsed.cpu_temp_critical,
				parsed.cpu_temp_warning,
				ntfy_server,
				parsed.update_rate,
			)
