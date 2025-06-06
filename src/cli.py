import argparse
import sys

from typing import Optional

_ntfy_configure_prompt = """\033[4mPlease configure an ntfy url before starting.\033[0m
Examples:
\033[32mpython3 main.py 10.0.13.37:42069
python3 main.py ntfy.domain.com\033[0m

Use \033[32m-h\033[0m or \033[32m--help\033[0m for a full list of options."""

class Interface:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument("--cpu-temp-disabled", action="store_true",   help="Disable notifications for CPU tempature.")
		self.parser.add_argument("--cpu-temp-critical", type=int,  default=80, help="CPU tempature for the crtitical alert. default = 80")
		self.parser.add_argument("--cpu-temp-warning",  type=int,  default=70, help="CPU tempature for the warning alert. default = 70")
		self.parser.add_argument("--update-rate",       type=int,  default=1,  help="How often updates happen in seconds. default = 1")

	def parsed_args(self):
		return self.parser.parse_args()

	def argv_1(self) -> Optional[str]:
		if len(sys.argv) > 1:
			return sys.argv[1]
		else:
			print(_ntfy_configure_prompt)
		return None