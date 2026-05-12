import datetime as dt
from enum import Enum
from sala import Sala

class Politica(Enum):
    """
    Enum que diferencia as estratégias utilizadas.
    """
    PRIO_DOCENTE = 1
    PRIO_PRIMEIRO = 2  

class Reserva:
    """
    Classe base de reserva. Toda a lógica principal da aplicação se encontra nela.    
    Suporte para reservas feitas no dia.

    Atributos:
    - reservas: lista de reservas feitas;
    - _salas: lista de salas ativas;
    - _usuarios: lista de usuarios ativos;
    - _politica: tipo de política de agendamento;
    - _horarios: lista de horários disponíveis divididos
    em intervalos de uma hora das 8:00 as 22:00.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Reserva, cls).__new__(cls)
            cls._instance.reservas = []
            cls._instance._salas = []
            cls._instance._usuarios = []
            cls._instance._politica = Politica.PRIO_PRIMEIRO
            cls._instance._horarios = []

            for i in range(8, 23):
                cls._horarios.append(str(dt.time(i, 0, 0)))

        return cls._instance
    
    def reservar(self, usuario, sala, hora):
        """
        Reserva uma sala de aula para um usuário
        dada a hora da reserva sendo ela um inteiro 
        no intervalo [8,22].
        """
        try:
            if hora < 8 or hora > 22:
                print("Horário indisponível para reserva.")
                return

            nova_reserva = {
                "usuario": usuario.name,
                "sala": sala.id,
                "hora": str(dt.time(hora, 0, 0))
            }

            if nova_reserva["hora"] in sala.disponibilidade:
                print("Sala {sala.id} já reservada nessa hora.")
                return

            sala.disponibilidade[nova_reserva["hora"]] = True
            self.reservas.append(nova_reserva)

            sala.registrar_observer(usuario)

            status = "confirmado"
            mensagem = f"Reserva da sala {sala.id} realizada pelo {usuario.name} as {nova_reserva["hora"]}"
            sala.notificar(mensagem)
            return
        except Exception as erro:
            status = "erro"
            mensagem = (
                f"Falha ao reservar a sala {getattr(sala, 'id', 'desconhecida')} "
                f"para {getattr(usuario, 'nome', 'usuário desconhecido')}. "
                f"Status: {status}. Motivo: {erro}"
            )
            

            sala.notificar(mensagem)

    def add_sala(self, s: Sala) -> None:
        """
        Adiciona uma sala a lista de salas ativas.
        """
        self._salas.append(s)

    def remove_sala(self, s: Sala) -> None:
        """
        Remove uma sala da lista de salas ativas.
        """
        try:
            self._salas.remove(s)
        except:
            print("Sala não existe.")

    def list_salas_disponiveis(self):
        """
        Lista as salas com horários disponíveis.
        """
        print('')
        print("--- Horários disponíveis para reserva ---")
        print('')
        for sala in self._salas:
            for horario in self._horarios:
                if horario not in sala.disponibilidade.keys():
                    print(f"Sala {sala.id} no {sala.local} disponível as {horario}")
