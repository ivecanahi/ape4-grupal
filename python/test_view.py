"""Pruebas de la Parte 3: exportación a CSV y gráfica."""

import csv
import tempfile
import unittest
from pathlib import Path

from datos_y_poblacion import SIRParameters, StepResult
from simulacion_simpy import SIRSimulation
from view import ChartView, CsvExporter

HEADER = "tiempo,susceptibles,infectados,recuperados"


class CsvExporterTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_exports_full_simulation(self) -> None:
        results = SIRSimulation(SIRParameters()).run()
        path = self.tmp / "salida" / "resultados.csv"

        CsvExporter.export(results, path)

        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], HEADER)
        self.assertEqual(len(lines) - 1, 101)
        self.assertEqual(lines[1], "0,95,5,0")
        with path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))[1:]
        for row in rows:
            self.assertEqual(sum(int(value) for value in row[1:]), 100)

    def test_exact_content_for_small_list(self) -> None:
        results = [StepResult(0, 9, 1, 0), StepResult(1, 8, 1, 1)]
        path = self.tmp / "pequeno.csv"

        CsvExporter.export(results, str(path))

        content = path.read_bytes().decode("utf-8")
        self.assertEqual(content, f"{HEADER}\r\n0,9,1,0\r\n1,8,1,1\r\n")


class ChartViewTest(unittest.TestCase):
    def test_creates_non_empty_image(self) -> None:
        results = SIRSimulation(SIRParameters()).run()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "graficas" / "sir.png"

            ChartView.plot(results, path)

            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
