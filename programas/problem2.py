def function_original(n: int) -> int:
    """Instrumented version of the program from problem 2."""
    if n <= 1:
        return 0
    counter = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            counter += 1
            break
    return counter


def operation_count(n: int) -> int:
    if n <= 1:
        return 0
    return n


if __name__ == "__main__":
    for value in [1, 10, 100, 1000]:
        print(f"n={value}, prints={operation_count(value)}")
