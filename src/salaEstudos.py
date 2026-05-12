from sala import Sala
from idGenerator import IDGenerator

class SalaDeEstudos(Sala):
	"""
	Subclasse de sala que representa uma sala de estudos.

	Atributos:
	- tem_lousa: flag que indica se a sala possui (True) ou não (False) uma lousa.
	"""
	def __init__(self, local: str, capacidade: int, tem_lousa: bool) -> None:
		self.id = IDGenerator().get()
		self.local = local
		self.tem_lousa = tem_lousa
		self.capacidade = capacidade
		self.disponibilidade = {}
		self._observers = []