from abc import ABCMeta

class Usuario(metaclass=ABCMeta):
	"""
	Classe base de usuário.

	Atributos: 
	- name: nome do usuário.
	"""
	name: str

	def recebe(self, msg: str) -> None:
		print(msg)