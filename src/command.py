import subprocess

def uname() -> str:
	return subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()