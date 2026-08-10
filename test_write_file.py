# write_file.py test cases

from functions.write_file import write_file


def test() -> None:
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # Test case 1:
    print(result)

    # Test case 2:
    print(f"{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}")

    # Test case 3:
    print(f"{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}")

if __name__ == "__main__":
    test()
