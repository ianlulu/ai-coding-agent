# get_file_content.py test cases

from functions.get_file_content import get_file_content


def test() -> None:
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    # test case 2:
    result = get_file_content("calculator", "main.py")
    print(f"{result}")

    # test case 3:
    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"{result}")

    # test case 4:
    result = get_file_content("calculator", "/bin/cat")
    print(f"{result}")

    # test case 5:
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"{result}")

if __name__ == "__main__":
    test()
