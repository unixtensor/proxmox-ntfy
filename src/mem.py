import psutil
import math

peak:  float = 0
check: int   = 3600 # Seconds

def usage() -> float:
	global peak
	mem = round(psutil.virtual_memory().used / 1048576000, 1)
	if mem > peak:
		peak = mem
	return mem

def total() -> int:
	return math.floor(psutil.virtual_memory().total / 1048576000)