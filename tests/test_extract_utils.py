import unittest
from netcdfGeo.extract import extract_from_mask, feature_transform
import numpy as np

# Example polygon feature with a hole


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
        crs_proj = {"proj": "lcc",
                    "lat_1": 46.8,
                    "lat_0": 46.8,
                    "lon_0": 0,
                    "k_0": 0.99987742,
                    "x_0": 600000,
                    "y_0": 2200000,
                    "a": 6378249.2,
                    "b": 6356515,
                    "units": "m",
                    "no_defs": True}
        crs_ll = {"proj": "longlat",
                  "ellps": "WGS84",
                  "datum": "WGS84",
                  "no_defs": True}
        # Perform round trip transformation 
        feature_proj = feature_transform(feature_polygon, crs_proj)
        feature_ll = feature_transform(feature_proj, crs_ll, crs_proj)
        # Compare polygon
        self.assertTrue(np.allclose(feature_polygon['geometry']['coordinates'][0],
                                    feature_ll['geometry']['coordinates'][0]))
        # Compare hole
        self.assertTrue(np.allclose(feature_polygon['geometry']['coordinates'][1],
                                    feature_ll['geometry']['coordinates'][1]))

if __name__ == '__main__':
    unittest.main()
