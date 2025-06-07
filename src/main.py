import time

import package
import cli
import cpu

from datetime import datetime
from typing import TypedDict
from ntfy import Ntfy

_pretty_date_time = datetime.fromtimestamp(time.time())
_monitoring_prompt = f"""{_pretty_date_time}
Ntfy monitoring software is now listening.

Source code available at:
<https://github.com/unixtensor/proxmox-ntfy>
<https://git.rhpidfyre.io/rhpidfyre/proxmox-ntfy>"""

class Config(TypedDict):
	cpu_temp_check_disabled: bool
	cpu_critical_temp:       int
	cpu_warning_temp:        int
	update_interval:         int
	ntfy_server_url:         str

def start(config: Config):
	ntfy = Ntfy(config["ntfy_server_url"])
	ntfy_cpu_temp_monitor = cpu.Tempature(ntfy, config["cpu_critical_temp"], config["cpu_warning_temp"])

	print(_monitoring_prompt)
	while True:
		if not config["cpu_temp_check_disabled"]:
			ntfy_cpu_temp_monitor.ntfy_check()
		time.sleep(config["update_interval"])

if __name__ == "__main__":
	if package.installed("lm-sensors"):
		cli_args = cli.Interface()
		start({
			"cpu_temp_check_disabled": cli_args.disable_cpu_temp,
			"cpu_critical_temp":       cli_args.cpu_temp_critical,
			"cpu_warning_temp":        cli_args.cpu_temp_warning,
			"update_interval":         cli_args.update_rate,
			"ntfy_server_url":         cli_args.server_address,
		})