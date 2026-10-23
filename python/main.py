from python.controller import SIRController
from python.model import SIRParameters


def main() -> None:
    params = SIRParameters()  # 100, 5, 0.30, 0.10, 100, semilla 42
    controller = SIRController(params)
    results = controller.run()

    last = results[-1]
    print("Simulación SIR finalizada correctamente.")
    print("Archivos creados: resultados_python.csv y grafica_sir_python.png")
    print(
        f"Tiempo final: {last.time} | "
        f"Susceptibles: {last.susceptible} | "
        f"Infectados: {last.infected} | "
        f"Recuperados: {last.recovered}"
    )


if __name__ == "__main__":
    main()
