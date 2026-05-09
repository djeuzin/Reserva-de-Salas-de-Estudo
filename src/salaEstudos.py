from sala import Sala
from idGenerator import IDGenerator

class SalaDeEstudos(Sala):
	def __init__(self, local: str, capacidade: int, tem_lousa: bool) -> None:
		self.id = IDGenerator().get()
		self.local = local
		self.tem_lousa = tem_lousa
		self.capacidade = capacidade