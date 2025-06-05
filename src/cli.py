import argparse

def interface():
	parser = argparse.ArgumentParser()
	parser.add_argument("--server", required=True, help="")
	parser.add_argument("--cpu-temp-critical", type=int, default=80, help="cpu tempature crtitical. default = 80")
	parser.add_argument("--cpu-temp-warning",  type=int, default=70, help="cpu tempature warning. default = 70")
	parser.add_argument("--update-rate",       type=int, default=1,  help="how often updates happen in seconds. default = 1")

	return parser.parse_args()