from abc import ABCMeta

class Usuario(metaclass=ABCMeta):
	name: str

	def recebe(self, msg: str) -> None:
		print(msg)