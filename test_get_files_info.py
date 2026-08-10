# get_files_info.py test cases

# import unittest
from functions.get_files_info import get_files_info


"""
class Test_get_files_info(unittest.TestCase):
    def setUp(self) -> None:
        return None

    def test_current_dir(self) -> None:
        result = get_files_info("calculator", ".")
        self.assertEqual()
"""

def test() -> None:
    print(
        "Result for current directory:"
    )
    print(f" {get_files_info("calculator", ".")}")

    print(
        "Result for 'pkg' directory:"
    )
    print(f" {get_files_info("calculator", "pkg")}")

    print(
        "Result for '/bin' directory:"
    )
    print(f" {get_files_info("calculator", "/bin")}")

    print(
        "Result for '../' directory:"
    )
    print(f" {get_files_info("calculator", "../")}")
    #print(get_files_info("calculator", "main.py"))

if __name__ == "__main__":
    test()
