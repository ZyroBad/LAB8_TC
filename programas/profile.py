import argparse
import contextlib
import csv
import html
import importlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time


N_VALUES = [1, 10, 100, 1000, 10000, 100000, 1000000]
PROBLEMS = [
    ("problema1", "problem1", "O(n^2 log n)"),
    ("problema2", "problem2", "O(n)"),
    ("problema3", "problem3", "O(n^2)"),
]
BASE = Path(__file__).resolve().parent
FIELDS = ["n", "operaciones", "estado", "tiempo_medido_segundos", "limite_segundos"]


def worker(module_name: str, n: int) -> None:
    module = importlib.import_module(module_name)
    # Keep print calls without filling the terminal or creating huge files.
    with open(os.devnull, "w", encoding="utf-8") as sink:
        with contextlib.redirect_stdout(sink):
            start = time.perf_counter()
            result = module.function_original(n)
            sink.flush()
            elapsed = time.perf_counter() - start
    if module_name == "problem1" and result != module.operation_count(n):
        raise RuntimeError("El contador no coincide con la formula")
    print(json.dumps({"seconds": elapsed}))


def measure(module_name: str, n: int, timeout: float) -> dict:
    operations = importlib.import_module(module_name).operation_count(n)
    row = dict(n=n, operaciones=operations, estado="completado",
               tiempo_medido_segundos="", limite_segundos=timeout)
    try:
        completed = subprocess.run(
            [sys.executable, "-B", str(Path(__file__).resolve()),
             "--worker", module_name, "--n", str(n)],
            capture_output=True, text=True, check=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        row["estado"] = "limite_excedido"
    else:
        row["tiempo_medido_segundos"] = f"{json.loads(completed.stdout)['seconds']:.12f}"
    return row


def svg_graph(name: str, complexity: str, rows: list[dict]) -> Path:
    completed = [r for r in rows if r["estado"] == "completado"]
    left, right, top, bottom = 100, 880, 90, 430
    values = [math.log10(max(float(r["tiempo_medido_segundos"]), 1e-12))
              for r in completed]
    low = math.floor(min(values)) if values else -6
    high = max(low + 1, math.ceil(max(values))) if values else 0

    def x(n):
        return left + math.log10(n) / 6 * (right - left)

    def y(v):
        return bottom - (v - low) / (high - low) * (bottom - top)

    elements = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="560" viewBox="0 0 960 560">',
                '<rect width="100%" height="100%" fill="white"/>',
                '<g font-family="Arial" fill="#222">',
                f'<text x="480" y="30" text-anchor="middle" font-size="20">{html.escape(name)} - {html.escape(complexity)}</text>',
                '<text x="480" y="55" text-anchor="middle" font-size="14">Ejecuciones completadas; escala log-log; salida a dispositivo nulo</text>']
    for power in range(low, high + 1):
        py = y(power)
        elements += [f'<line x1="{left}" y1="{py}" x2="{right}" y2="{py}" stroke="#ddd"/>',
                     f'<text x="{left-12}" y="{py+4}" text-anchor="end" font-size="12">1e{power}</text>']
    for n in N_VALUES:
        elements.append(f'<text x="{x(n)}" y="455" text-anchor="middle" font-size="12">{n}</text>')
    elements += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222"/>',
                 f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222"/>',
                 '<text x="25" y="260" transform="rotate(-90 25 260)" text-anchor="middle" font-size="14">Tiempo medido (s)</text>',
                 '<text x="480" y="482" text-anchor="middle" font-size="14">n</text>']
    # Do not connect points across inputs that did not finish.
    segment = []
    for row in rows + [{"estado": "fin"}]:
        if row["estado"] != "completado":
            if segment:
                points = " ".join(segment)
                elements.append(f'<polyline points="{points}" fill="none" stroke="#087f8c" stroke-width="2"/>')
                segment = []
            continue
        px = x(row["n"])
        py = y(math.log10(max(float(row["tiempo_medido_segundos"]), 1e-12)))
        segment.append(f"{px},{py}")
        elements.append(f'<circle cx="{px}" cy="{py}" r="5" fill="#087f8c"/>')
    missing = ", ".join(str(r["n"]) for r in rows if r["estado"] != "completado") or "ninguno"
    elements.append(f'<text x="480" y="515" text-anchor="middle" font-size="13">Limite excedido (sin punto): n = {missing}</text>')
    elements.append('</g></svg>')
    path = BASE / "graficas" / f"{name}.svg"
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(elements), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Profiling real con limite por ejecucion")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--worker", choices=[p[1] for p in PROBLEMS], help=argparse.SUPPRESS)
    parser.add_argument("--n", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout debe ser positivo y finito")
    if args.worker:
        if args.n is None:
            parser.error("el worker necesita --n")
        worker(args.worker, args.n)
        return
    report = ["# Resultados de profiling real", "",
              f"Limite por proceso: {args.timeout:g} s. Cada entrada se intenta una vez.",
              "Tiempo medido dentro de la funcion, incluyendo flush de salida; excluye arranque de Python.",
              "El limite incluye el arranque del proceso. Un limite excedido no es un tiempo medido ni una estimacion.",
              "Las impresiones se ejecutan y se redirigen al dispositivo nulo; no se mide el renderizado de terminal.", ""]
    for name, module_name, complexity in PROBLEMS:
        rows = []
        print(f"{name}: {complexity}", flush=True)
        for n in N_VALUES:
            row = measure(module_name, n, args.timeout)
            rows.append(row)
            print(f"  n={n}: {row['estado']} {row['tiempo_medido_segundos']}", flush=True)
        path = BASE / "resultados" / f"{name}.csv"
        path.parent.mkdir(exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        svg_graph(name, complexity, rows)
        report += [f"## {name} - {complexity}", "",
                   "| n | Operaciones | Tiempo medido (s) | Estado |",
                   "| --- | --- | --- | --- |"]
        report += [f"| {r['n']} | {r['operaciones']} | {r['tiempo_medido_segundos'] or '-'} | {r['estado']} |" for r in rows]
        report.append("")
    (BASE / "resultados" / "resumen.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
