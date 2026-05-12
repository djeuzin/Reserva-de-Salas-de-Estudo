from usuario import Usuario

class Professor(Usuario):
	"""
	Subclasse de usuário que representa um docente.

	Atributos:
	- matricula: identificador único do docente.
	"""
	def __init__(self, name: str, matricula: int) -> None:
		self.name = name
		self.matricula = matricula