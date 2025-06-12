import requests

from typing import TypedDict, Optional
from print_t import print_t
from enum import Enum

class HeaderPriority(Enum):
	Urgent = "5"
	High   = "4"
	Medium = "3"
	Low    = "2"
	Min    = "1"

class Headers(TypedDict):
	Priority: HeaderPriority
	Title: str
	Tags: str

class Ntfy:
	def __init__(self, server: str, logging_disabled: bool):
		self.server = server
		self.logging_disabled = logging_disabled

	def send(self, message: str, title: Optional[str] = None, extra_headers: Optional[Headers] = None):
		headers = {}
		if title:
			headers["Title"] = title.encode(encoding="utf-8")
		if extra_headers:
			headers.update(extra_headers)
		if not self.logging_disabled:
			print_t(f"Ntfy OUT: \033[0;35mtitle\033[0m={title} \033[0;35mmessage\033[0m={message} \033[0;35mheaders\033[0m={headers}")
		try:
			requests.post(self.server, data=message.encode(encoding="utf-8"), headers=headers)
		except Exception as err:
			print_t(f"\033[31m{err}\033[0m")
