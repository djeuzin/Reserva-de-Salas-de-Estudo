from sala import Sala

class SalaDeAula(Sala):
	def __init__(self, local: str, capacidade: str) -> None:
		self.local = local
		self.capacidade = capacidade
		self.id = generate_id()