import argparse


def function_original(n: int) -> int:
    """Instrumented version of the nested-loop program from problem 1."""
    counter = 0
    for i in range(n // 2, n + 1):
        for j in range(1, n - n // 2 + 1):
            k = 1
            while k <= n:
                counter += 1
                k *= 2
    return counter


def operation_count(n: int) -> int:
    """Exact number of counter++ executions without expanding the loops."""
    if n < 1:
        return 0
    i_count = n - (n // 2) + 1
    j_count = n - (n // 2)
    k_count = n.bit_length()
    return i_count * j_count * k_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    args = parser.parse_args()
    print(function_original(args.n))
