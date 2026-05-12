from abc import ABCMeta, abstractmethod

class EstrategiaFila(metaclass=ABCMeta):
    """
    Interface base para estratégias de ordenação da fila de reservas.
    """
    @abstractmethod
    def ordenar(self, fila: list) -> list:
        pass

class FilaFIFO(EstrategiaFila):
    """
    Estratégia de fila por ordem de chegada.
    Nenhuma reordenação é aplicada.
    """
    def ordenar(self, fila: list) -> list:
        return list(fila)

class FilaPrioDocente(EstrategiaFila):
    """
    Estratégia de fila com prioridade a professores.
    Professores são movidos para a frente mantendo
    a ordem de chegada entre usuários do mesmo tipo.
    """
    def ordenar(self, fila: list) -> list:
        from professor import Professor
        docentes = [req for req in fila if isinstance(req[0], Professor)]
        demais   = [req for req in fila if not isinstance(req[0], Professor)]
        return docentes + demais