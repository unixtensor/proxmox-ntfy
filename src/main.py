import time
import re

import command
import cli
import cpu

from datetime import datetime
from typing   import TypedDict
from ntfy     import Ntfy

def start_prompt(server_url: str) -> str:
	return f"""{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Listening and sending notifications to: \033[32m{server_url}\033[0m.

Source code available at:
* <https://github.com/unixtensor/proxmox-ntfy>
<https://git.rhpidfyre.io/rhpidfyre/proxmox-ntfy>
------"""

class Address:
	def __init__(self, address: str):
		self.address = address

	def is_valid(self) -> bool:
		return re.search(r"^\d+[.]\d+[.]\d+[.]\d+|^(https|http)://.+$", self.address) != None

	def format(self, topic: str) -> str:
		addr = self.address
		if self.address[len(self.address)-1] != "/":
			addr += "/"
		return addr + topic

	def not_valid_prompt(self) -> str:
		return f"""The address "{self.address}" is not valid.
Accepted address types:
\033[32m10.0.0.69:42069
http://domain.com
https://domain.com\033[0m

Address with a topic:
\033[32m10.0.0.69:42069\033[0m -t|--topic \033[32mexample_topic\033[0m
\033[32mhttp://domain.com\033[0m -t|--topic \033[32mexample_topic\033[0m
\033[32mhttps://domain.com\033[0m -t|--topic \033[32mexample_topic\033[0m"""

class Config(TypedDict):
	cpu_temp_critical_timeout: int
	cpu_temp_critical_message: str
	cpu_temp_warning_timeout:  int
	cpu_temp_warning_message:  str
	cpu_temp_check_disabled:   bool
	startup_notify_disabled:   bool
	startup_notify_message:    str
	ntfy_logs_disabled:        bool
	cpu_temp_critical:         int
	cpu_warning_temp:          int
	update_interval:           int
	ntfy_server_url:           str

class Init:
	def __init__(self, config: Config):
		self.config           = config
		self.ntfy             = Ntfy(config["ntfy_server_url"], config["ntfy_logs_disabled"])
		self.monitor_cpu_temp = cpu.Tempature(self.ntfy)
		cpu.Tempature.warning_message    = config["cpu_temp_warning_message"]
		cpu.Tempature.timeout_check_warn = config["cpu_temp_warning_timeout"]
		cpu.Tempature.thermal_warn_c     = config["cpu_warning_temp"]

	def __listen(self):
		while True:
			if not self.config["cpu_temp_check_disabled"]:
				self.monitor_cpu_temp.ntfy_check()
			time.sleep(self.config["update_interval"])

	def __start_notify(self):
		t = datetime.now()
		self.ntfy.send(
			message=command.uname(),
			title=self.config["startup_notify_message"] + f" {t.strftime('%Y-%m-%d')} - {t.strftime('%H:%M:%S')}")

	def start(self):
		if self.config["cpu_warning_temp"] >= self.config["cpu_temp_critical"]:
			print("CPU warning tempature cannot be greater than or equal to the crtitical tempature.")
			return

		print(f"{self.config}\n" + start_prompt(self.config["ntfy_server_url"]))

		if not self.config["startup_notify_disabled"]:
			self.__start_notify()
		self.__listen()

def main():
	cli_args = cli.Interface()
	address  = Address(cli_args.server_address_no_topic)
	if address.is_valid():
		Init({
			"cpu_temp_critical_timeout": cli_args.cpu_temp_critical_timeout,
			"cpu_temp_critical_message": cli_args.cpu_temp_critical_message,
			"cpu_temp_warning_timeout":  cli_args.cpu_temp_warning_timeout,
			"cpu_temp_warning_message":  cli_args.cpu_temp_warning_message,
			"cpu_temp_check_disabled":   cli_args.disable_cpu_temp,
			"startup_notify_disabled":   cli_args.disable_startup_notify,
			"startup_notify_message":    cli_args.startup_notify_message,
			"ntfy_logs_disabled":        cli_args.disable_ntfy_logs,
			"cpu_temp_critical":         cli_args.cpu_temp_critical,
			"cpu_warning_temp":          cli_args.cpu_temp_warning,
			"update_interval":           cli_args.update_rate,
			"ntfy_server_url":           address.format(cli_args.topic)
		}).start()
	else:
		print(address.not_valid_prompt())

if __name__ == "__main__":
	if command.package_installed("lm-sensors"):
		main()