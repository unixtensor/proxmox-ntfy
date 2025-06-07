import argparse

import cpu

def Interface():
	parser = argparse.ArgumentParser()
	parser.add_argument("server_address", help="The ntfy server address.")

	parser.add_argument("--disable-uptime-notifys", action="store_true", help="Disable uptime notifications.")
	parser.add_argument("--disable-startup-ping",   action="store_true", help="Disable the start up ping.")
	parser.add_argument("--disable-cpu-temp",       action="store_true", help="Disable notifications for CPU tempature.")

	parser.add_argument("--cpu-temp-warning", type=int,  default=70, help="CPU tempature for the warning alert. default = 70")
	parser.add_argument("--update-rate",      type=int,  default=1,  help="How often updates happen in seconds. default = 1")

	parser.add_argument("--cpu-temp-warning-message", default=cpu.Tempature.cpu_temp_warning_message, help="The notification message if the CPU is at a high tempature. (message) [TEMP] C")
	parser.add_argument("--startup-ping-message",     default="🖥️ Ntfy proxmox monitoring started.",  help="The notification message when the program is started.")

	return parser.parse_args()