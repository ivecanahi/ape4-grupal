"""Parte 2: Simulación con SimPy del modelo SIR.

Implementa la clase SIRSimulation, que ejecuta el modelo SIR en tiempo
discreto usando SimPy. Depende de las clases definidas en
Datos_poblacion.py (Parte 1).
"""

import random

import simpy

from datos_y_poblacion  import State, SIRParameters, StepResult, Population


class SIRSimulation:
    """Simulación del modelo SIR sobre SimPy.

    Atributos:
        params: Parámetros del modelo (población, beta, gamma, etc.).
        rng: Generador aleatorio con semilla fija (reproducibilidad).
        population: Estado actual de la población.
        env: Entorno de simulación de SimPy.
        results: Lista de StepResult registrados en cada instante.
    """

    def __init__(self, params: SIRParameters) -> None:
        self.params = params
        self.rng = random.Random(params.seed)
        self.population = Population(
            size=params.population,
            initial_infected=params.initial_infected,
            rng=self.rng,
        )
        self.env = simpy.Environment()
        self.results: list[StepResult] = []

    # Registro y lógica de un paso

    def _record(self) -> None:
        """Guarda el conteo actual de S, I, R en el instante actual."""
        susceptible, infected, recovered = self.population.count()
        self.results.append(
            StepResult(
                time=int(self.env.now),
                susceptible=susceptible,
                infected=infected,
                recovered=recovered,
            )
        )

    def _step(self) -> None:
        """Aplica un paso de contagio y recuperación sobre el snapshot.

        Los cambios se calculan sobre una copia del estado para evitar
        que un individuo contagiado en este paso pueda contagiar a otro
        dentro del mismo paso.
        """
        snapshot = self.population.snapshot()
        self._spread_infections(snapshot)
        self._recover_infected(snapshot)

    def _spread_infections(self, snapshot: list[State]) -> None:
        """Cada infectado elige un contacto al azar y lo contagia con prob. beta."""
        for index, state in enumerate(snapshot):
            if state != State.INFECTED:
                continue
            contact = self.population.random_contact(index)
            if snapshot[contact] != State.SUSCEPTIBLE:
                continue
            if self.rng.random() < self.params.beta:
                self.population.set_state(contact, State.INFECTED)

    def _recover_infected(self, snapshot: list[State]) -> None:
        """Cada infectado al inicio del paso se recupera con prob. gamma."""
        for index, state in enumerate(snapshot):
            if state != State.INFECTED:
                continue
            if self.rng.random() < self.params.gamma:
                self.population.set_state(index, State.RECOVERED)


    # Bucle de simulación y ejecución

    def _process(self):
        """Generador de SimPy: registra y avanza el tiempo hasta max_time."""
        while self.env.now < self.params.max_time:
            self._record()
            self._step()
            yield self.env.timeout(1)
        # Registro final en t = max_time (última fila del CSV)
        self._record()

    def run(self) -> list[StepResult]:
        """Ejecuta la simulación y devuelve la lista de resultados."""
        self.env.process(self._process())
        self.env.run()
        return self.results