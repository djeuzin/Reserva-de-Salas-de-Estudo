# Reserva de Salas de Estudo

**Rafael Freire Machado Gonçalves — 163977**  
**João Victor Rocha — 163837**

Projeto da disciplina de Projeto Orientado a Objetos, primeiro semestre de 2026.

---

## Descrição

Sistema de reserva de salas universitárias via linha de comando, inteiramente em memória. Permite que múltiplos usuários (alunos e professores) tentem reservar salas simultaneamente, com controle de concorrência por mutex e política de prioridade configurável.

---

## Como executar

```bash
cd src
python main.py
```

Não há dependências externas além da biblioteca padrão do Python (3.10+).

---

## Padrões de projeto aplicados

### Singleton
`Reserva` e `IDGenerator` utilizam o padrão Singleton, garantindo uma única instância compartilhada entre todas as threads da aplicação.

### Factory Method
`SalaFactory` e `UsuarioFactory` encapsulam a criação de objetos polimórficos. O chamador passa um enum (`TipoDeSala`, `TipoDeUsuario`) e recebe a instância concreta correspondente sem conhecer sua classe diretamente.

### Observer
`Sala` mantém uma lista de observadores (`_observers`) e os notifica via `notificar()` após cada evento de reserva. `Usuario` implementa o lado receptor com o método `recebe()`, imprimindo a confirmação ou erro da reserva.

### Strategy
`Reserva` delega a ordenação da fila de requisições a uma estratégia intercambiável (`EstrategiaFila`). Duas implementações estão disponíveis:

- `FilaFIFO` — ordem de chegada (primeiro a solicitar, primeiro a ser atendido).
- `FilaPrioDocente` — professores são movidos para a frente da fila; entre usuários do mesmo tipo, a ordem de chegada é preservada.

A política pode ser definida na instanciação ou alterada em tempo de execução via `set_estrategia()`.

---

## Concorrência

Cada usuário é simulado por uma thread independente. O acesso ao método `reservar()` é serializado por busy-wait sobre um lock interno ao singleton `Reserva`. As requisições são enfileiradas e reordenadas conforme a política ativa antes de serem processadas.

---

## Estrutura do projeto

```
.
├── docs/
│   └── Diagrama UML.pdf
├── src/
│   ├── main.py            # Ponto de entrada; cria threads e simula reservas simultâneas
│   ├── reserva.py         # Singleton central; controle de concorrência e fila
│   ├── estrategia.py      # Strategy: EstrategiaFila, FilaFIFO, FilaPrioDocente
│   ├── sala.py            # Classe abstrata Sala (Observer subject)
│   ├── salaEstudos.py     # Subclasse: Sala de Estudos
│   ├── salaAula.py        # Subclasse: Sala de Aula
│   ├── laboratorio.py     # Subclasse: Laboratório
│   ├── salaFactory.py     # Factory de salas
│   ├── usuario.py         # Classe abstrata Usuario (Observer listener)
│   ├── aluno.py           # Subclasse: Aluno
│   ├── professor.py       # Subclasse: Professor
│   ├── usuarioFactory.py  # Factory de usuários
│   └── id_generator.py    # Singleton gerador de IDs sequenciais
└── README.md
```