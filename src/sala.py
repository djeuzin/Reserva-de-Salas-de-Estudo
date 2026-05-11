from abc import ABCMeta

class Sala(metaclass=ABCMeta):
	capacidade: int
	local: str
	_id: int
	disponibilidade: dict[int, bool]
	_observers: list

	def __init__(self):
		self._observers = []

	def registrar_observer(self, observer):
		"""Registra um observador"""
		if observer not in self._observers:
			self._observers.append(observer)

	def remover_observer(self, observer):
		"""Remove um observador"""
		if observer in self._observers:
			self._observers.remove(observer)
