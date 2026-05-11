from usuario import Usuario

class Aluno(Usuario):
	def __init__(self, name: str, cpf: str):
		self.name = name
		self.cpf = cpf

	def notificar(self, sala, mensagem: str):
		print(f"[NOTIFICAÇÃO] Aluno {self.name} recebeu mensagem da sala {getattr(sala, 'id', 'desconhecida')}: {mensagem}")