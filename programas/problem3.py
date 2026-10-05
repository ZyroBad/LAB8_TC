def function_original(n: int) -> int:
    """Instrumented version of the nested-loop program from problem 3."""
    counter = 0
    for i in range(1, n // 3 + 1):
        for j in range(1, n + 1, 4):
            counter += 1
    return counter


def operation_count(n: int) -> int:
    if n < 1:
        return 0
    i_count = n // 3
    j_count = (n + 3) // 4
    return i_count * j_count


if __name__ == "__main__":
    for value in [1, 10, 100, 1000]:
        print(f"n={value}, prints={operation_count(value)}")
