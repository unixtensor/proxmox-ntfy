import time

import command
import cli
import cpu

from datetime import datetime
from address  import Address
from typing   import TypedDict
from ntfy     import Ntfy

class Prompt:
	@staticmethod
	def start(address: str) -> str:
			return f"""{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Listening and sending notifications to: \033[32m{address}\033[0m.

Source code available at:
* <https://github.com/unixtensor/proxmox-ntfy>
<https://git.rhpidfyre.io/rhpidfyre/proxmox-ntfy>
------"""

	@staticmethod
	def address_not_valid(address: str) -> str:
			return f"""The address "{address}" is not valid.
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
		if not self.config["startup_notify_disabled"]:
			self.__start_notify()
		self.__listen()

def main():
	cli_args = cli.Interface()
	address  = Address(cli_args.server_address_no_topic)
	if address.is_valid():
		formatted_address = address.format(cli_args.topic)
		print(Prompt.start(formatted_address))

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
			"ntfy_server_url":           formatted_address
		}).start()
	else:
		print(Prompt.address_not_valid(cli_args.server_address_no_topic))

if __name__ == "__main__":
	if command.package_installed("lm-sensors"):
		main()