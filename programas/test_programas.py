import contextlib
import io
import unittest

import problem1
import problem2
import problem3
import profile as profiling


class ProgramTests(unittest.TestCase):
    def test_problem1_counter(self):
        for n in [0, 1, 2, 3, 7, 8, 9, 10, 31, 32, 33, 100]:
            with self.subTest(n=n):
                self.assertEqual(problem1.function_original(n), problem1.operation_count(n))

    def test_printed_sequences(self):
        for module in [problem2, problem3]:
            for n in [0, 1, 2, 3, 4, 7, 10, 33]:
                with self.subTest(module=module.__name__, n=n):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        module.function_original(n)
                    self.assertEqual(output.getvalue(), "Sequence\n" * module.operation_count(n))

    def test_measured_execution(self):
        for module in ["problem1", "problem2", "problem3"]:
            row = profiling.measure(module, 10, 5)
            self.assertEqual(row["estado"], "completado")
            self.assertGreater(float(row["tiempo_medido_segundos"]), 0)

    def test_timeout_has_no_fake_measurement(self):
        row = profiling.measure("problem1", 1000000, 0.2)
        self.assertEqual(row["estado"], "limite_excedido")
        self.assertEqual(row["tiempo_medido_segundos"], "")


if __name__ == "__main__":
    unittest.main()
