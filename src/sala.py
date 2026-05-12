from abc import ABCMeta

class Sala(metaclass=ABCMeta):
	capacidade: int
	local: str
	id: int
	disponibilidade: dict[str, bool]
	_observers: list

	def registrar_observer(self, observer):
		"""Registra um observador"""
		if observer not in self._observers:
			self._observers.append(observer)

	def remover_observer(self, observer):
		"""Remove um observador"""
		if observer in self._observers:
			self._observers.remove(observer)

	def notificar(self, msg: str):
		for obs in self._observers:
			obs.recebe(msg)