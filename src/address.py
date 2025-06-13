import re

class Address:
	def __init__(self, address: str):
		self.address = address

	def is_valid(self) -> bool:
		return re.search(r"^\d+[.]\d+[.]\d+[.]\d+|^(https|http)://.+$", self.address) != None

	def format(self, topic: str) -> str:
		addr = self.address
		if self.address[len(self.address)-1] != "/":
			addr += "/"
		return addr + topic