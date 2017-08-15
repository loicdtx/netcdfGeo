import unittest
from netcdfGeo.extract import extract_from_mask
import numpy as np

# Example polygon feature with a hole
feature_polygon = {'geometry': {'coordinates': [[[5.02, 45.319],
                                                 [5.201, 45.217],
                                                 [5.134, 45.074],
                                                 [5.494, 45.071],
                                                 [5.464, 44.793],
                                                 [5.825, 44.7],
                                                 [5.641, 44.651],
                                                 [5.597, 44.543],
                                                 [5.664, 44.501],
                                                 [5.418, 44.424],
                                                 [5.631, 44.331],
                                                 [5.678, 44.146],
                                                 [5.454, 44.119],
                                                 [5.15, 44.235],
                                                 [5.166, 44.314],
                                                 [4.825, 44.228],
                                                 [4.65, 44.329],
                                                 [4.886, 44.936],
                                                 [4.8, 45.298],
                                                 [5.02, 45.319]],
                                                [[4.97, 44.429],
                                                 [4.889, 44.304],
                                                 [5.07, 44.376],
                                                 [4.97, 44.429]]],
                                'type': 'Polygon'},
                   'properties': {'name': 'drome'},
                   'type': 'Feature'}


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

    def test_feature_transform(self):
        


if __name__ == '__main__':
    unittest.main()
