import time

import package
import cli
import cpu

from datetime import datetime
from typing import TypedDict
from ntfy import Ntfy

def start_prompt(server_url: str) -> str:
	return f"""{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Listening and sending notifications to: \033[32m{server_url}\033[0m.

Source code available at:
<https://github.com/unixtensor/proxmox-ntfy>
<https://git.rhpidfyre.io/rhpidfyre/proxmox-ntfy>
------"""

class Config(TypedDict):
	cpu_temp_warning_message: str
	cpu_temp_check_disabled:  bool
	startup_ping_disabled:    bool
	startup_ping_message:     str
	cpu_warning_temp:         int
	update_interval:          int
	ntfy_server_url:          str

class Init:
	def __init__(self, config: Config):
		self.config           = config
		self.ntfy             = Ntfy(config["ntfy_server_url"])
		self.monitor_cpu_temp = cpu.Tempature(self.ntfy, config["cpu_warning_temp"])

		cpu.Tempature.cpu_temp_warning_message = config["cpu_temp_warning_message"]

	def __listen(self):
		while True:
			if not self.config["cpu_temp_check_disabled"]:
				self.monitor_cpu_temp.ntfy_check()
			time.sleep(self.config["update_interval"])

	def start(self):
		print(f"{self.config}\n" + start_prompt(self.config["ntfy_server_url"]))

		if not self.config["startup_ping_disabled"]:
			self.ntfy.send(self.config["startup_ping_message"])

		self.__listen()

if __name__ == "__main__":
	if package.installed("lm-sensors"):
		cli_args = cli.Interface()
		Init({
			"cpu_temp_warning_message": cli_args.cpu_temp_warning_message,
			"cpu_temp_check_disabled":  cli_args.disable_cpu_temp,
			"startup_ping_disabled":    cli_args.disable_startup_ping,
			"startup_ping_message":     cli_args.startup_ping_message,
			"cpu_warning_temp":         cli_args.cpu_temp_warning,
			"update_interval":          cli_args.update_rate,
			"ntfy_server_url":          cli_args.server_address,
		}).start()