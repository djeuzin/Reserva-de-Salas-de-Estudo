import datetime as dt
import threading
from sala import Sala
from estrategia import EstrategiaFila, FilaFIFO
import json

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
    _init_lock = threading.Lock()

    def __new__(cls):
        with cls._init_lock:
            if cls._instance is None:
                cls._instance = super(Reserva, cls).__new__(cls)
                cls._instance.reservas = []
                cls._instance._salas = []
                cls._instance._usuarios = []
                cls._instance._horarios = []
                cls._instance._fila = []
                cls._instance._fila_lock = threading.Lock()
                cls._instance._lock = threading.Lock()
                cls._instance._estrategia = FilaFIFO()

                for i in range(8, 23):
                    cls._instance._horarios.append(str(dt.time(i, 0, 0)))

        return cls._instance
    
    def reservar(self, usuario, sala, hora, barreira: threading.Barrier = None):
        """
        Reserva uma sala de aula para um usuário
        dada a hora da reserva sendo ela um inteiro 
        no intervalo [8,22].

        A fila de usuários é ordenada conforme a estratégia ativa (fila ou fila de
        prioridade). Ao chegar para reservar, o usuário fica em espera ocupada 
        esperando sua vez na fila para tentar realizar a reserva.
        """

        requisicao = (usuario, sala, hora)

        with self._fila_lock:
            self._fila.append(requisicao)

        if barreira:
            barreira.wait()

        while True:
            if self._lock.acquire(blocking=False):
                try:
                    with self._fila_lock:
                        fila_ordenada = self._estrategia.ordenar(self._fila)

                    if fila_ordenada[0] is not requisicao:
                        continue

                    self._processar(usuario, sala, hora)

                    with self._fila_lock:
                        self._fila.remove(requisicao)
                finally:
                    self._lock.release()
                break

    def _processar(self, usuario, sala, hora: int) -> None:
        """
        Executa a reserva de acordo com os padrões seguidos.
        """
        if hora < 8 or hora > 22:
            sala.notificar(f"[ERRO] Horário {hora}h inválido para reserva.")
            return

        horario_str = str(dt.time(hora, 0, 0))

        if horario_str in sala.disponibilidade:
            sala.notificar(
                f"[NEGADO] Sala {sala.id} já reservada às {horario_str}. "
                f"Solicitante: {usuario.name}."
            )
            return

        sala.disponibilidade[horario_str] = True
        self.reservas.append({
            "usuario": usuario.name,
            "sala": sala.id,
            "hora": horario_str
        })

        sala.registrar_observer(usuario)
        sala.notificar(
            f"[OK] Reserva confirmada — sala {sala.id} às {horario_str} "
            f"para {usuario.name}."
        )

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

    def set_estrategia(self, strat: EstrategiaFila) -> None:
        """
        Seta a politica para utilizar na reserva de salas.
        """
        self._estrategia = strat

    def cancelar(self, usuario, sala, hora: int) -> bool:
        """
        Cancela uma reserva existente do usuário e notifica todos os observers da sala.
        """
        horario_str = str(dt.time(hora, 0, 0))

        reserva = next(
            (r for r in self.reservas
             if r["usuario"] == usuario.name
             and r["sala"] == sala.id
             and r["hora"] == horario_str),
            None
        )

        if reserva is None:
            usuario.recebe(f"[ERRO] Nenhuma reserva encontrada para cancelar.")
            return False

        self.reservas.remove(reserva)
        del sala.disponibilidade[horario_str]

        sala.notificar(
            f"[CANCELADO] Reserva da sala {sala.id} às {horario_str} "
            f"cancelada por {usuario.name}."
        )

        return True

    def alterar(self, usuario, sala, hora_antiga: int, hora_nova: int) -> None:
        if not self.cancelar(usuario, sala, hora_antiga):
            usuario.recebe(f"[ERRO] Nenhuma reserva encontrada para alterar.")
            return

        self.reservar(usuario, sala, hora_nova)

    def gerar_relatorio(self) -> None:
        try:
            with open('daily_report.json', 'w') as file:
                json.dump(self.reservas, file, ensure_ascii=False, indent=2)
                print("Relatório daily_report.json gerado.")
        except:
            print("Erro ao tentar gerar relatório.")
