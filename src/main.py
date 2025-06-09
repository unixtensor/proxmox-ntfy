import time
import re

import package
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

	def valid(self) -> bool:
		if re.search(r"^\d+[.]\d+[.]\d+[.]\d+", self.address):
			return True
		elif re.search(r"^(https|http)://.+$", self.address):
			return True
		return False

	def format(self, topic: str) -> str:
		return self.address + "/" + topic

	def not_valid_prompt(self) -> str:
		return f"""The address "{self.address}" is not valid.
Accepted address types:
\033[32m10.0.0.69:42069
http://domain.com
https://domain.com\033[0m

Address with a topic:
\033[32m10.0.0.69:42069 -t|--topic example_topic
http://domain.com -t|--topic example_topic
https://domain.com -t|--topic example_topic\033[0m"""

class Config(TypedDict):
	cpu_temp_warning_timeout: int
	cpu_temp_warning_message: str
	cpu_temp_check_disabled:  bool
	startup_notify_disabled:  bool
	startup_notify_message:   str
	ntfy_logs_disabled:       bool
	cpu_warning_temp:         int
	update_interval:          int
	ntfy_server_url:          str

class Init:
	def __init__(self, config: Config):
		self.config           = config
		self.ntfy             = Ntfy(config["ntfy_server_url"], config["ntfy_logs_disabled"])
		self.monitor_cpu_temp = cpu.Tempature(self.ntfy, config["cpu_warning_temp"])
		cpu.Tempature.warning_message = config["cpu_temp_warning_message"]
		cpu.Tempature.timeout_check   = config["cpu_temp_warning_timeout"]

	def __listen(self):
		while True:
			if not self.config["cpu_temp_check_disabled"]:
				self.monitor_cpu_temp.ntfy_check()
			time.sleep(self.config["update_interval"])

	def start(self):
		print(f"{self.config}\n" + start_prompt(self.config["ntfy_server_url"]))

		if not self.config["startup_notify_disabled"]:
			self.ntfy.send(self.config["startup_notify_message"])
		self.__listen()

def main():
	cli_args = cli.Interface()
	address  = Address(cli_args.server_address_no_topic)
	if address.valid():
		Init({
			"cpu_temp_warning_timeout": cli_args.cpu_temp_warning_timeout,
			"cpu_temp_warning_message": cli_args.cpu_temp_warning_message,
			"cpu_temp_check_disabled":  cli_args.disable_cpu_temp,
			"startup_notify_disabled":  cli_args.disable_startup_notify,
			"startup_notify_message":   cli_args.startup_notify_message,
			"ntfy_logs_disabled":       cli_args.disable_ntfy_logs,
			"cpu_warning_temp":         cli_args.cpu_temp_warning,
			"update_interval":          cli_args.update_rate,
			"ntfy_server_url":          address.format(cli_args.topic)
		}).start()
	else:
		print(address.not_valid_prompt())

if __name__ == "__main__":
	if package.installed("lm-sensors"):
		main()