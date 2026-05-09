from usuario import Usuario

class Aluno(Usuario):
	def __init__(self, name: str, cpf: str):
		self.name = name
		self.cpf = cpf