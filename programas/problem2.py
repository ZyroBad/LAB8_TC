import argparse


def function_original(n: int) -> None:
    """Instrumented version of the program from problem 2."""
    if n <= 1:
        return
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print("Sequence")
            break


def operation_count(n: int) -> int:
    if n <= 1:
        return 0
    return n


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    args = parser.parse_args()
    function_original(args.n)
