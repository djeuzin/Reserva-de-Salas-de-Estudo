from usuario import Usuario

class Professor(Usuario):
	def __init__(self, name: str, matricula: int) -> None:
		self.name = name
		self.matricula = matricula