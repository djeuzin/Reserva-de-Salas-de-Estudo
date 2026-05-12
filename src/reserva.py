import datetime as dt
from enum import Enum
from sala import Sala

class Politica(Enum):
    PRIO_DOCENTE = 1
    PRIO_PRIMEIRO = 2  

class Reserva:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Reserva, cls).__new__(cls)
            cls._instance.reservas = []
            cls._salas = []
            cls._usuarios = []
            cls._politica = Politica.PRIO_PRIMEIRO
            cls._horarios = []

            for i in range(8, 23):
                cls._horarios.append(str(dt.time(i, 0, 0)))

        return cls._instance
    
    def reservar(self, usuario, sala, hora):
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
        self._salas.append(s)

    def remove_sala(self, s: Sala) -> None:
        try:
            self._salas.remove(s)
        except:
            print("Sala não existe.")

    def list_salas_disponiveis(self):
        print('')
        print("--- Horários disponíveis para reserva ---")
        print('')
        for sala in self._salas:
            for horario in self._horarios:
                if horario not in sala.disponibilidade.keys():
                    print(f"Sala {sala.id} no {sala.local} disponível as {horario}")
