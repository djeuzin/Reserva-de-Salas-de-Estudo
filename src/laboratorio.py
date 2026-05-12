from sala import Sala
from idGenerator import IDGenerator

class Laboratorio(Sala):
	def __init__(self, local: str, capacidade: str, qtd_maquinas: int) -> None:
		self.local = local
		self.capacidade = capacidade
		self.qtd_maquinas = qtd_maquinas
		self.id = IDGenerator().get()
		self.disponibilidade = {}
		self._observers = []