"""Parte 3: exportación de resultados a CSV y gráfica S(t), I(t), R(t)."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Backend sin ventana, solo para guardar archivos
import matplotlib.pyplot as plt  # noqa: E402

from datos_y_poblacion import StepResult  # noqa: E402

HEADER = ["tiempo", "susceptibles", "infectados", "recuperados"]


class CsvExporter:
    """Escribe los resultados de la simulación en un archivo CSV."""

    @staticmethod
    def export(results: list[StepResult], path) -> None:
        """Guarda una fila por instante con el encabezado de la guía."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)
            for step in results:
                writer.writerow(
                    [step.time, step.susceptible, step.infected, step.recovered]
                )


class ChartView:
    """Genera la gráfica de S(t), I(t) y R(t)."""

    @staticmethod
    def plot(results: list[StepResult], path) -> None:
        """Dibuja las tres curvas y guarda la imagen en `path`."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        times = [step.time for step in results]

        fig, ax = plt.subplots()
        ax.plot(times, [s.susceptible for s in results], label="Susceptibles", color="green")
        ax.plot(times, [s.infected for s in results], label="Infectados", color="red")
        ax.plot(times, [s.recovered for s in results], label="Recuperados", color="gray")
        ax.set_title("Modelo SIR (Python + SimPy)")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Individuos")
        ax.legend()
        ax.grid(True)
        fig.savefig(path, dpi=150)
        plt.close(fig)
