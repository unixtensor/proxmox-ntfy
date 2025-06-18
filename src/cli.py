import argparse

import cpu

from typing import TypedDict

class Config(TypedDict):
	cpu_temp_critical_timeout: int
	cpu_temp_critical_message: str
	cpu_temp_warning_timeout:  int
	cpu_temp_warning_message:  str
	cpu_temp_check_disabled:   bool
	cpu_temp_critical:         int
	cpu_warning_temp:          int
	cpu_temp_zone_label:       str
	cpu_temp_zone:             str
	startup_notify_disabled:   bool
	startup_notify_message:    str
	daily_notifys_disabled:    bool
	ntfy_logs_disabled:        bool
	update_interval:           int
	ntfy_server_url:           str

class Interface:
	def __init__(self):
		parser = argparse.ArgumentParser(
			prog="Proxmox monitoring",
			description="Proxmox monitoring tool for phone notifications using ntfy.sh")

		parser.add_argument("server_address_no_topic", help="The ntfy server address.")

		parser.add_argument("-t", "--topic", default="proxmox", help="The ntfy topic name that notifications will be sent to. Default = proxmox")
		parser.add_argument("--update-rate", type=int, default=1, help="How often updates happen in seconds. default = 1")

		parser.add_argument("--disable-uptime-notifys", action="store_true", help="Disable uptime notifications.")
		parser.add_argument("--disable-startup-notify", action="store_true", help="Disable the start up notify.")
		parser.add_argument("--disable-daily-notifys",  action="store_true", help="Disable the daily notifys on the system's highest stats.")
		parser.add_argument("--disable-cpu-temp",       action="store_true", help="Disable notifications for CPU tempature.")
		parser.add_argument("--disable-ntfy-logs",      action="store_true", help="Disable logging ntfy activity to the output.")

		parser.add_argument("--cpu-temp-zone", default="k10temp", help="The tempature zone for getting CPU info. default = k10temp")
		parser.add_argument("--cpu-temp-zone-label", default="Tctl", help="The label for getting the current CPU tempature. default = Tctl")

		parser.add_argument("--cpu-temp-warning", type=int, default=cpu.Tempature.thermal_warn_c, help=f"CPU tempature for the warning alert. default = {cpu.Tempature.thermal_warn_c}")
		parser.add_argument("--cpu-temp-warning-timeout", type=int, default=cpu.Tempature.timeout_check_warn, help=f"Timeout in seconds until another CPU tempature related notification can be pushed. default = {cpu.Tempature.timeout_check_warn}")
		parser.add_argument("--cpu-temp-warning-message", default=cpu.Tempature.warning_message, help="The notification message if the CPU is at a high tempature. (message) [TEMP] C")

		parser.add_argument("--cpu-temp-critical", type=int, default=cpu.Tempature.thermal_critical_c, help=f"CPU tempature for the critical alert. default = {cpu.Tempature.thermal_critical_c}")
		parser.add_argument("--cpu-temp-critical-timeout", type=int, default=cpu.Tempature.timeout_check_critical, help=f"Timeout in seconds until another CPU tempature related notification can be pushed. default = {cpu.Tempature.timeout_check_critical}")
		parser.add_argument("--cpu-temp-critical-message", default=cpu.Tempature.critical_message, help="The notification message if the CPU is at a high tempature. (message) [TEMP] C")

		parser.add_argument("--startup-notify-message", default="🖥️ Ntfy proxmox monitoring started.", help="The notification message when the program is started.")

		self.cli_args = parser.parse_args()

	def to_config(self, formatted_address: str) -> Config:
		return {
			"cpu_temp_critical_timeout": self.cli_args.cpu_temp_critical_timeout,
			"cpu_temp_critical_message": self.cli_args.cpu_temp_critical_message,
			"cpu_temp_warning_timeout":  self.cli_args.cpu_temp_warning_timeout,
			"cpu_temp_warning_message":  self.cli_args.cpu_temp_warning_message,
			"cpu_temp_check_disabled":   self.cli_args.disable_cpu_temp,
			"cpu_temp_critical":         self.cli_args.cpu_temp_critical,
			"cpu_warning_temp":          self.cli_args.cpu_temp_warning,
			"cpu_temp_zone_label":       self.cli_args.cpu_temp_zone_label,
			"cpu_temp_zone":             self.cli_args.cpu_temp_zone,
			"startup_notify_disabled":   self.cli_args.disable_startup_notify,
			"daily_notifys_disabled":    self.cli_args.disable_daily_notifys,
			"startup_notify_message":    self.cli_args.startup_notify_message,
			"ntfy_logs_disabled":        self.cli_args.disable_ntfy_logs,
			"update_interval":           self.cli_args.update_rate,
			"ntfy_server_url":           formatted_address
		}