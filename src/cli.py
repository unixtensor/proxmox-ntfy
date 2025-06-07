import argparse

def Interface():
	parser = argparse.ArgumentParser()
	parser.add_argument("server_address", help="The ntfy server address.")

	parser.add_argument("--disable-uptime-notifys", action="store_true", help="Disable uptime notifications.")
	parser.add_argument("--disable-cpu-temp",       action="store_true", help="Disable notifications for CPU tempature.")
	parser.add_argument("--cpu-temp-warning", type=int,  default=70, help="CPU tempature for the warning alert. default = 70")
	parser.add_argument("--update-rate",      type=int,  default=1,  help="How often updates happen in seconds. default = 1")

	return parser.parse_args()