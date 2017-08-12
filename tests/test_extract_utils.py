import unittest
from netcdfGeo.extract import extract_from_mask
import numpy as np

class TestExtractUtils(unittest.TestCase):

    def test_extract_from_mask(self):
        array = np.array(range(1, 19), dtype=np.float32).reshape((2,3,3))
        mask = np.array([[False, False, True],
                         [False, True, True],
                         [True, False, False]])
        expected_mean = np.array([4.8, 13.8], dtype=np.float32)
        expected_median = np.array([4, 13], dtype=np.float32)
        expected_sum = np.array([24, 69], dtype=np.float32)
        expected_max = np.array([9, 18], dtype=np.float32)
        expected_min = np.array([1, 10], dtype=np.float32)
        self.assertTrue(np.allclose(extract_from_mask(array, mask, 'mean'), expected_mean))
        self.assertTrue(np.allclose(extract_from_mask(array, mask, 'median'), expected_median))
        self.assertTrue(np.allclose(extract_from_mask(array, mask, 'max'), expected_max))
        self.assertTrue(np.allclose(extract_from_mask(array, mask, 'min'), expected_min))
        self.assertTrue(np.allclose(extract_from_mask(array, mask, 'sum'), expected_sum))
        with self.assertRaises(ValueError):
            extract_from_mask(array, mask, 'sd')


if __name__ == '__main__':
    unittest.main()
