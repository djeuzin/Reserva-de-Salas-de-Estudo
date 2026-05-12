import threading
from salaFactory import SalaFactory, TipoDeSala
from usuarioFactory import UsuarioFactory, TipoDeUsuario
from estrategia import FilaFIFO, FilaPrioDocente
from reserva import Reserva

def tentar_reservar(usuario, sala, hora):
    Reserva().reservar(usuario, sala, hora)

def main():
    # -------------------------------------------------------------------
    # Demonstração 1: FilaFIFO — ordem de chegada
    # -------------------------------------------------------------------
    print("=" * 55)
    print("  POLÍTICA: FIFO (primeiro a chegar, primeiro atendido)")
    print("=" * 55)

    gerente = Reserva()

    sala = SalaFactory().get_instance(TipoDeSala.LABORATORIO, "Dep. Computacao", 40, 20)
    gerente.add_sala(sala)

    aluno1    = UsuarioFactory().get_instance(TipoDeUsuario.ALUNO,     "Carlos",    111111)
    aluno2    = UsuarioFactory().get_instance(TipoDeUsuario.ALUNO,     "Beatriz",   222222)
    prof1     = UsuarioFactory().get_instance(TipoDeUsuario.PROFESSOR, "Dra. Ana",  999001)
    prof2     = UsuarioFactory().get_instance(TipoDeUsuario.PROFESSOR, "Dr. Mario", 999002)

    # Todos tentam reservar o mesmo horário simultaneamente.
    threads = [
        threading.Thread(target=tentar_reservar, args=(aluno1, sala, 10)),
        threading.Thread(target=tentar_reservar, args=(aluno2, sala, 10)),
        threading.Thread(target=tentar_reservar, args=(prof1,  sala, 10)),
        threading.Thread(target=tentar_reservar, args=(prof2,  sala, 10)),
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print()
    gerente.list_salas_disponiveis()

    # -------------------------------------------------------------------
    # Demonstração 2: FilaPrioDocente — professores na frente
    # Troca de estratégia em tempo de execução.
    # -------------------------------------------------------------------
    print()
    print("=" * 55)
    print("  POLÍTICA: PRIORIDADE DOCENTE")
    print("=" * 55)

    gerente.set_estrategia(FilaPrioDocente())

    sala2 = SalaFactory().get_instance(TipoDeSala.SALA_ESTUDOS, "Biblioteca", 15, True)
    gerente.add_sala(sala2)

    aluno3 = UsuarioFactory().get_instance(TipoDeUsuario.ALUNO,     "Diego",     333333)
    aluno4 = UsuarioFactory().get_instance(TipoDeUsuario.ALUNO,     "Fernanda",  444444)
    prof3  = UsuarioFactory().get_instance(TipoDeUsuario.PROFESSOR, "Dra. Lena", 999003)

    threads2 = [
        threading.Thread(target=tentar_reservar, args=(aluno3, sala2, 14)),
        threading.Thread(target=tentar_reservar, args=(aluno4, sala2, 14)),
        threading.Thread(target=tentar_reservar, args=(prof3,  sala2, 14)),
    ]

    for t in threads2:
        t.start()
    for t in threads2:
        t.join()

    print()
    gerente.list_salas_disponiveis()

    print()
    print("=" * 55)
    print("  CANCELAMENTO DE RESERVA")
    print("=" * 55)
 
    gerente.alterar(aluno3, sala2, 14, 15)
 
    print()
    gerente.list_salas_disponiveis()

    gerente.gerar_relatorio()

if __name__ == "__main__":
    main()