from datetime import datetime

class Reserva:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Reserva, cls).__new__(cls)
            cls._instance.reservas = []
        return cls._instance
    
    def add_sala(self, usuario, sala, data_hora):
        try:
            nova_reserva = {
                "usuario": usuario.nome,
                "sala": sala.id,
                "data_hora": data_hora.strftime("%Y-%m-%d %H:%M")
            }
            self.reservas.append(nova_reserva)

            status = "confirmado"
            mensagem = f"Reserva da sala {sala.id} realizada pelo {usuario.nome}. Status: {status}"
            sala.notificar(mensagem)
            return status
        except Exception as erro:
            status = "erro"
            mensagem = (
                f"Falha ao reservar a sala {getattr(sala, 'id', 'desconhecida')} "
                f"para {getattr(usuario, 'nome', 'usuário desconhecido')}. "
                f"Status: {status}. Motivo: {erro}"
            )
            if hasattr(sala, "notificar"):
                sala.notificar(mensagem)
            else:
                print(mensagem)
            return status
