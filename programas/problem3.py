import argparse


def function_original(n: int) -> None:
    """Instrumented version of the nested-loop program from problem 3."""
    for i in range(1, n // 3 + 1):
        for j in range(1, n + 1, 4):
            print("Sequence")


def operation_count(n: int) -> int:
    if n < 1:
        return 0
    i_count = n // 3
    j_count = (n + 3) // 4
    return i_count * j_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    args = parser.parse_args()
    function_original(args.n)
