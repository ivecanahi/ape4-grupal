
import random
from dataclasses import dataclass
from enum import Enum


# ---------------------------------------------------------------------------
# PARTE 1 – Datos y población
# ---------------------------------------------------------------------------

class State(Enum):
    """Estados posibles de un individuo del modelo SIR."""

    SUSCEPTIBLE = "S"
    INFECTED = "I"
    RECOVERED = "R"


@dataclass(frozen=True)
class SIRParameters:
    """Parámetros comunes del modelo, los mismos en Python y NetLogo."""

    population: int = 100
    initial_infected: int = 5
    beta: float = 0.30
    gamma: float = 0.10
    max_time: int = 100
    seed: int = 42


@dataclass(frozen=True)
class StepResult:
    """Conteo de S, I y R registrado en un instante de tiempo."""

    time: int
    susceptible: int
    infected: int
    recovered: int


class Population:
    """Conjunto de individuos S, I o R."""

    def __init__(self, size: int, initial_infected: int, rng: random.Random) -> None:
        self.size = size
        self._rng = rng
        self._states = [State.SUSCEPTIBLE] * size
        for index in rng.sample(range(size), initial_infected):
            self._states[index] = State.INFECTED

    def count(self) -> tuple[int, int, int]:
        """Devuelve (S, I, R)."""
        return (
            self._states.count(State.SUSCEPTIBLE),
            self._states.count(State.INFECTED),
            self._states.count(State.RECOVERED),
        )

    def snapshot(self) -> list[State]:
        """Copia del estado actual, para calcular los cambios de un paso sobre ella."""
        return list(self._states)

    def random_contact(self, index: int) -> int:
        """Índice de un individuo al azar"""
        # Se elige entre size - 1 posiciones y se salta `index`: una sola llamada al rng.
        contact = self._rng.randrange(self.size - 1)
        return contact + 1 if contact >= index else contact

    def set_state(self, index: int, state: State) -> None:
        self._states[index] = state
