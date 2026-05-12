class Singleton:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance

class IDGenerator(Singleton):
	"""
	Classe para gerar IDs de salas.

	Atributos:
	- id: Identificador que será retornado.
	"""
	id: int = 10

	def get(self) -> int:
		"""
		Método que retorna um id que pode ser utilizado.
		Incrementa o id corrente para posteriores chamadas.
		"""
		self.id = self.id + 1
		return self.id - 1