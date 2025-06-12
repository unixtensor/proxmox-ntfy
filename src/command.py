import subprocess

from typing import Optional

def package_installed(package_name: str) -> Optional[bool]:
	try:
		installed = subprocess.run(["dpkg", "-s", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
		if not installed:
			print(f"Package \"{package_name}\" not installed.")
		return installed
	except Exception as err:
		print(f"\033[31m{err}\033[0m")
		return None

def uname() -> str:
	return subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()