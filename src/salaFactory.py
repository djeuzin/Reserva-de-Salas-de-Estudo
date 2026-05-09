from sala import Sala
from laboratorio import Laboratorio
from salaAula import SalaDeAula
from salaEstudos import SalaDeEstudos
from enum import Enum

class TipoDeSala(Enum):
	SALA_ESTUDOS = 1
	SALA_AULA = 2
	LABORATORIO = 3

class SalaFactory:
	def get_instance(self, tipo_de_sala: int, local: str, capacidade: int, other: any = None) -> Sala:
		match tipo_de_sala:
			case TipoDeSala.SALA_ESTUDOS:
				return SalaDeEstudos(local, capacidade, other)
			case TipoDeSala.SALA_AULA:
				return SalaDeAula(local, capacidade)
			case TipoDeSala.LABORATORIO:
				return Laboratorio(local, capacidade, other)
			case _:
				raise ValueError("Valor inválido.")