from usuario import Usuario
from professor import Professor
from aluno import Aluno
from enum import Enum

class TipoDeUsuario(Enum):
	ALUNO = 1
	PROFESSOR = 2

class UsuarioFactory:
	def get_instance(self, tipo_de_usuario: TipoDeUsuario, name: str, other: any) -> Usuario:
		match tipo_de_usuario:
			case TipoDeUsuario.ALUNO:
				return Aluno(name, other)
			case TipoDeUsuario.PROFESSOR:
				return Professor(name, other)
			case _:
				raise ValueError("Valor inválido.")