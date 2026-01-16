
# tests to verify services functions

from services import calculate_status

def run_tests():
    assert calculate_status(50) == "OK"
    assert calculate_status(10) == "LOW STOCK"
    assert calculate_status(0) == "OUT OF STOCK"
    print("All tests passed")

if __name__ == "__main__":
    run_tests()
