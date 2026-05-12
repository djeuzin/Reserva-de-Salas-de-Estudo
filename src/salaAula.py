from sala import Sala
from idGenerator import IDGenerator

class SalaDeAula(Sala):
	"""
	Subclasse de sala que representa uma sala de aula.
	"""
	def __init__(self, local: str, capacidade: str) -> None:
		self.local = local
		self.capacidade = capacidade
		self.id = IDGenerator().get()
		self.disponibilidade = {}
		self._observers = []