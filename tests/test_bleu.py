import unittest
from speciallectureis.calculate_oracle_bleu import calculate_oracle_bleu


class TestCalculateOracleBleu(unittest.TestCase):
    def test_not_found_hyps(self):
        with self.assertRaises(FileNotFoundError):
            calculate_oracle_bleu("not_exist.txt", "refs.txt", 2, [1, 2], "exp")

    def test_not_found_refs(self):
        with self.assertRaises(FileNotFoundError):
            calculate_oracle_bleu("hyps.txt", "not_exist.txt", 2, [1, 2], "exp")

    def test_oracle_bleu(self):
        oracles = calculate_oracle_bleu("hyps.txt", "refs.txt", 2, [1, 2], "exp")
        self.assertEqual(["38.13", "82.48"], oracles)
