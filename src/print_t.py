from datetime import datetime

def print_t(out: str):
	t = datetime.now()
	print(f"({t.strftime('%Y-%m-%d')})[{t.strftime('%H:%M:%S')}]: " + out)