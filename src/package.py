import subprocess

from typing import Optional

def installed(package_name: str) -> Optional[bool]:
	try:
		installed = subprocess.run(["dpkg", "-s", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0
		if not installed:
			print(f"Package \"{package_name}\" not installed.")
		return installed
	except Exception as err:
		print(err)
		return None

def installed_list(package_name_list: list[str]) -> bool:
	for pkg_name in package_name_list:
		if not installed(pkg_name):
			return False
	return True