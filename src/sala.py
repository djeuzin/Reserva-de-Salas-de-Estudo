from abc import ABCMeta

class Sala(metaclass=ABCMeta):
	"""
	Classe base de uma sala que pode ser reservada.

	Atributos:
	- capacidade: quantidade de alunos comportados pela sala;
	- local: localização no campus;
	- id: identificador único da sala;
	- disponibilidade: dicionário que indica quais reservas foram feitas;
	- _observers: lista de instâncias que observam a sala.
	"""
	capacidade: int
	local: str
	id: int
	disponibilidade: dict[str, bool]
	_observers: list

	def registrar_observer(self, observer):
		"""
		Registra um observador.
		"""
		if observer not in self._observers:
			self._observers.append(observer)

	def remover_observer(self, observer):
		"""
		Remove um observador.
		"""
		if observer in self._observers:
			self._observers.remove(observer)

	def notificar(self, msg: str):
		"""
		Notifica os observadores da sala.
		"""
		for obs in self._observers:
			obs.recebe(msg)