import argparse
import sys

from typing import Optional

_ntfy_configure_prompt = """\033[4mPlease configure an ntfy url before starting.\033[0m
Examples:
\033[32mpython3 main.py 10.0.13.37:42069
python3 main.py ntfy.domain.com\033[0m"""

class Interface:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument("--cpu-temp-critical", type=int, default=80, help="cpu tempature crtitical. default = 80")
		self.parser.add_argument("--cpu-temp-warning",  type=int, default=70, help="cpu tempature warning. default = 70")
		self.parser.add_argument("--update-rate",       type=int, default=1,  help="how often updates happen in seconds. default = 1")

	def parsed_args(self):
		return self.parser.parse_args()

	def argv_1(self) -> Optional[str]:
		if len(sys.argv) > 1:
			return sys.argv[1]
		else:
			print(_ntfy_configure_prompt)
		return None