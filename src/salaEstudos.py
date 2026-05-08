from sala import Sala

class SalaDeEstudos(Sala):
	def __init__(self, local: str, capacidade: int, tem_lousa: bool) -> None:
		self.id = generate_id()
		self.local = local
		self.tem_lousa = tem_lousa
		self.capacidade = capacidade