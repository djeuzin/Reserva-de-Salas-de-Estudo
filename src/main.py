from salaFactory import SalaFactory, TipoDeSala
from usuarioFactory import UsuarioFactory, TipoDeUsuario
from reserva import Reserva

def main():
	gerente = Reserva()

	sala = SalaFactory().get_instance(TipoDeSala.LABORATORIO, "Dep. Computacao", 40, 20)
	user = UsuarioFactory().get_instance(TipoDeUsuario.ALUNO, "Rafael", 163977)

	gerente.add_sala(sala)

	gerente.list_salas_disponiveis()

	gerente.reservar(user, sala, 8)

	gerente.list_salas_disponiveis()

if __name__ == "__main__":
	main()