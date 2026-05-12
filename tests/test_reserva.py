import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, ROOT)

from aluno import Aluno
from reserva import Reserva
from salaEstudos import SalaDeEstudos

import pytest

@pytest.fixture(autouse=True)
def reset_reserva_instance():
    Reserva._instance = None
    yield
    Reserva._instance = None


def test_cria_aluno():
    aluno = Aluno("Carlos", "111111")

    assert aluno.name == "Carlos"
    assert aluno.cpf == "111111"


def test_reserva_sala_sucesso():
    reserva = Reserva()
    sala = SalaDeEstudos("Biblioteca", 15, True)
    reserva.add_sala(sala)
    aluno = Aluno("Carlos", "111111")

    reserva.reservar(aluno, sala, 10)

    assert sala.disponibilidade == {"10:00:00": True}
    assert reserva.reservas == [
        {"usuario": "Carlos", "sala": sala.id, "hora": "10:00:00"}
    ]
    assert reserva._salas == [sala]


def test_cancelar_reserva_sucesso():
    reserva = Reserva()
    sala = SalaDeEstudos("Biblioteca", 15, True)
    reserva.add_sala(sala)
    aluno = Aluno("Carlos", "111111")

    reserva.reservar(aluno, sala, 10)
    resultado = reserva.cancelar(aluno, sala, 10)

    assert resultado is True
    assert sala.disponibilidade == {}
    assert reserva.reservas == []
