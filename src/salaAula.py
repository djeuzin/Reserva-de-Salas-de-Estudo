from sala import Sala
from idGenerator import IDGenerator

class SalaDeAula(Sala):
	def __init__(self, local: str, capacidade: str) -> None:
		self.local = local
		self.capacidade = capacidade
		self.id = IDGenerator().get()