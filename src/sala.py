from abc import ABCMeta

class Sala(metaclass=ABCMeta):
	capacidade: int
	local: str
	_id: int