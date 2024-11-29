import unittest
from causalpathalgorithms import PaCo, PaCo2
from utils import read_time_stamped_csv


class TestPaco(unittest.TestCase):

    _, test_edges = read_time_stamped_csv("data/test-edges.csv", "numeric")
    expected_test_csv_result = {
        ("a", "b"): 2,
        ("b", "c"): 2,
        ("c", "d"): 1,
        ("d", "c"): 2,
        ("c", "b"): 1,
        ("b", "a"): 1,
        ("a", "b", "a"): 2,
        ("a", "b", "c"): 2,
        ("b", "c", "d"): 1,
        ("c", "b", "c"): 1,
        ("d", "c", "b"): 1,
        ("d", "c", "d"): 2,
    }

    def test_paco_on_example(self):
        result = PaCo(self.test_edges, 2, 2)
        self.assertDictEqual(
            result, self.expected_test_csv_result, f"Test results of PaCo don't match "
        )

    def test_paco_2_on_example(self):
        result = PaCo2(self.test_edges, 2, 2)
        self.assertDictEqual(
            result, self.expected_test_csv_result, f"Test results of PaCo don't match "
        )


if __name__ == "__main__":
    unittest.main()
