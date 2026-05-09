class Singleton:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance

class IDGenerator(Singleton):
	id: int = 10

	def get(self) -> int:
		self.id = self.id + 1
		return self.id - 1