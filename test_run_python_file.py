# run_python_file.py test cases

from functions.run_python_file import run_python_file


def test() -> None:
    # Test case 1:
    test_run: str = run_python_file("calculator", "main.py")
    print(test_run)

    # Test case 2:
    test_run: str = run_python_file("calculator", "main.py", ["3 + 5"])
    print(test_run)

    # Test case 3:
    test_run: str = run_python_file("calculator", "tests.py")
    print(test_run)

    # Test case 4:
    test_run: str = run_python_file("calculator", "../main.py") # should return an error
    print(test_run)

    # Test case 5:
    test_run: str = run_python_file("calculator", "nonexistent.py") # should return an error
    print(test_run)

    # Test case 6:
    test_run: str = run_python_file("calculator", "lorem.txt") # should return an error
    print(test_run)

if __name__ == "__main__":
    test()
