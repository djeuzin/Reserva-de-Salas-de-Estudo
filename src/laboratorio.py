from sala import Sala

class Laboratorio(Sala):
	def __init__(self, local: str, capacidade: str, qtd_maquinas: int) -> None:
		self.local = local
		self.capacidade = capacidade
		self.qtd_maquinas = qtd_maquinas
		self.id = generate_id()