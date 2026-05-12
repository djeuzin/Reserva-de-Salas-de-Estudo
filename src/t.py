import datetime as dt
import threading
from sala import Sala
from estrategia import EstrategiaFila, FilaFIFO

class Reserva:
    """
    Singleton central da aplicação. Gerencia salas, usuários e reservas.

    Suporte a reservas concorrentes via busy-wait sobre um lock interno.
    A ordem de atendimento da fila é definida por uma EstrategiaFila
    intercambiável.

    Atributos:
    - reservas: lista de reservas confirmadas;
    - _salas: lista de salas ativas;
    - _horarios: horários disponíveis das 8:00 às 22:00;
    - _lock: threading.Lock que serializa o acesso à seção crítica;
    - _fila: lista de requisições pendentes (usuario, sala, hora);
    - _fila_lock: lock auxiliar para acesso seguro à fila;
    - _estrategia: instância de EstrategiaFila em uso.
    """
    _instance = None
    _init_lock = threading.Lock()

    def __new__(cls, estrategia: EstrategiaFila = None):
        with cls._init_lock:
            if cls._instance is None:
                cls._instance = super(Reserva, cls).__new__(cls)
                cls._instance.reservas = []
                cls._instance._salas = []
                cls._instance._horarios = [
                    str(dt.time(h, 0, 0)) for h in range(8, 23)
                ]
                cls._instance._lock = threading.Lock()
                cls._instance._fila = []
                cls._instance._fila_lock = threading.Lock()
                cls._instance._estrategia = estrategia if estrategia else FilaFIFO()
        return cls._instance

    def set_estrategia(self, estrategia: EstrategiaFila) -> None:
        """
        Substitui a estratégia de ordenação da fila em tempo de execução.
        """
        self._estrategia = estrategia

    def reservar(self, usuario, sala, hora: int, barreira: threading.Barrier = None) -> None:
        """
        Enfileira uma requisição de reserva e aguarda sua vez via busy-wait.

        O parâmetro opcional `barreira` sincroniza threads para que todas
        estejam na fila antes de qualquer uma começar a disputar o lock —
        tornando a política de ordenação observável na saída.

        A fila é reordenada conforme a estratégia ativa a cada iteração
        do busy-wait, de modo que mudanças de política em tempo de execução
        são respeitadas.
        """
        requisicao = (usuario, sala, hora)

        with self._fila_lock:
            self._fila.append(requisicao)

        # Aguarda todas as threads estarem enfileiradas antes de competir.
        if barreira:
            barreira.wait()

        # Busy-wait: tenta adquirir o lock; se não conseguir, volta ao loop.
        while True:
            if self._lock.acquire(blocking=False):
                try:
                    with self._fila_lock:
                        fila_ordenada = self._estrategia.ordenar(self._fila)

                    # Só processa se esta requisição for a cabeça da fila.
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
        Executa a reserva propriamente dita. Chamado apenas dentro do lock.
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
        """Adiciona uma sala à lista de salas ativas."""
        self._salas.append(s)

    def remove_sala(self, s: Sala) -> None:
        """Remove uma sala da lista de salas ativas."""
        try:
            self._salas.remove(s)
        except ValueError:
            print("Sala não encontrada.")

    def list_salas_disponiveis(self) -> None:
        """Lista todos os horários ainda disponíveis para cada sala ativa."""
        print()
        print("--- Horários disponíveis para reserva ---")
        print()
        for sala in self._salas:
            for horario in self._horarios:
                if horario not in sala.disponibilidade:
                    print(f"Sala {sala.id} em '{sala.local}' disponível às {horario}")