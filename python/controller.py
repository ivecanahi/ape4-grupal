from pathlib import Path

from .model import SIRParameters, SIRSimulation
from .view import CsvExporter, ChartView


class SIRController:
    """Conecta el modelo de simulación con sus vistas de salida."""

    def __init__(self, params: SIRParameters, output_dir: str | Path = ".") -> None:
        self.params = params
        self.output_dir = Path(output_dir)

    def run(self):
        """Ejecuta el modelo, guarda el CSV y crea la gráfica."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        simulation = SIRSimulation(self.params)
        results = simulation.run()

        csv_path = self.output_dir / "resultados_python.csv"
        chart_path = self.output_dir / "grafica_sir_python.png"

        CsvExporter().export(results, str(csv_path))
        ChartView().plot(results, str(chart_path))

        return results
