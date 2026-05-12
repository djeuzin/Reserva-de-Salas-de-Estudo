from usuario import Usuario

class Aluno(Usuario):
	"""
	Subclasse de usuário que representa um aluno.

	Atributos:
	- cpf: identificador único do aluno.
	"""
	def __init__(self, name: str, cpf: str):
		self.name = name
		self.cpf = cpf