import csv
import importlib
import math
import time
from pathlib import Path


N_VALUES = [1, 10, 100, 1000, 10000, 100000, 1000000]
PROBLEMS = [
    ("problema1", "problem1", "O(n^2 log n)"),
    ("problema2", "problem2", "O(n)"),
    ("problema3", "problem3", "O(n^2)"),
]
RESULTS_DIR = Path(__file__).parent / "resultados"
GRAPHS_DIR = Path(__file__).parent / "graficas"


def calibrate_ops_per_second(iterations: int = 2_000_000) -> float:
    total = 0
    start = time.perf_counter()
    for i in range(iterations):
        total += i & 1
    elapsed = time.perf_counter() - start
    if total < 0:
        print("unreachable")
    return iterations / elapsed


def measure_call(fn, n: int, repetitions: int = 7) -> float:
    best = float("inf")
    for _ in range(repetitions):
        start = time.perf_counter()
        fn(n)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best


def write_csv(problem_name: str, rows: list[dict[str, str]]) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / f"{problem_name}.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "n",
                "operaciones",
                "tiempo_estimado_segundos",
                "tiempo_medicion_formula_segundos",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    return path


def svg_graph(problem_name: str, complexity: str, rows: list[dict[str, str]]) -> Path:
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 900, 520
    margin_left, margin_bottom, margin_top, margin_right = 80, 70, 45, 35
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    xs = [math.log10(float(row["n"])) for row in rows]
    ys = [math.log10(max(float(row["tiempo_estimado_segundos"]), 1e-12)) for row in rows]
    raw_xs = [float(row["n"]) for row in rows]
    raw_ys = [max(float(row["tiempo_estimado_segundos"]), 1e-12) for row in rows]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    def scale_x(x: float) -> float:
        return margin_left + (x - min_x) / (max_x - min_x) * plot_w

    def scale_y(y: float) -> float:
        return margin_top + (1 - (y - min_y) / (max_y - min_y)) * plot_h

    points = [(scale_x(x), scale_y(y)) for x, y in zip(xs, ys)]
    polyline = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    circles = "\n".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="#0f766e" />'
        for x, y in points
    )
    x_labels = "\n".join(
        f'<text x="{x:.2f}" y="{height - 38}" text-anchor="middle" font-size="12">{int(n)}</text>'
        for (x, _), n in zip(points, raw_xs)
    )
    point_labels = "\n".join(
        f'<text x="{x:.2f}" y="{y - 10:.2f}" text-anchor="middle" font-size="11">{seconds:.3g}s</text>'
        for (x, y), seconds in zip(points, raw_ys)
    )

    path = GRAPHS_DIR / f"{problem_name}.svg"
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{width / 2}" y="28" text-anchor="middle" font-family="Arial" font-size="20" font-weight="700">{problem_name} - {complexity} (escala log-log)</text>
  <line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="#334155" stroke-width="2"/>
  <line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#334155" stroke-width="2"/>
  <text x="22" y="{height / 2}" transform="rotate(-90 22 {height / 2})" text-anchor="middle" font-family="Arial" font-size="14">Tiempo estimado (s)</text>
  <text x="{width / 2}" y="{height - 10}" text-anchor="middle" font-family="Arial" font-size="14">n</text>
  <polyline fill="none" stroke="#0f766e" stroke-width="3" points="{polyline}"/>
  {circles}
  {x_labels}
  {point_labels}
  <text x="{margin_left}" y="{height - margin_bottom + 24}" font-family="Arial" font-size="12">min={min(raw_ys):.6g}s</text>
  <text x="{width - margin_right}" y="{margin_top + 18}" text-anchor="end" font-family="Arial" font-size="12">max={max(raw_ys):.6g}s</text>
</svg>
""",
        encoding="utf-8",
    )
    return path


def main() -> None:
    ops_per_second = calibrate_ops_per_second()
    print(f"Calibracion local: {ops_per_second:,.0f} operaciones/segundo")

    for problem_name, module_name, complexity in PROBLEMS:
        module = importlib.import_module(module_name)
        rows = []
        for n in N_VALUES:
            operations = module.operation_count(n)
            measured_formula = measure_call(module.operation_count, n)
            estimated = operations / ops_per_second
            rows.append(
                {
                    "n": str(n),
                    "operaciones": str(operations),
                    "tiempo_estimado_segundos": f"{estimated:.10f}",
                    "tiempo_medicion_formula_segundos": f"{measured_formula:.10f}",
                }
            )
        csv_path = write_csv(problem_name, rows)
        svg_path = svg_graph(problem_name, complexity, rows)
        print(f"{problem_name}: {csv_path} | {svg_path}")


if __name__ == "__main__":
    main()
