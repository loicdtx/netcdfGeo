import numpy as np
from pyproj import Proj, transform

import copy

def extract_from_mask(array, mask, fun='mean', sp_axes=(1,2)):
    """Extract and spatially aggregate data from a 3D array using a 2D mask

    Args:
        array (np.array): Input 3D array from which values have to be extracted and
            spatially summarized
        mask (np.array): 2D mask (array of booleans) matching the spatial dimensions
            of the input 3D. True correspond to masked cells.
        fun (str): Aggregating function (any of 'mean', 'max', 'min', 'median')
        sp_axes (tupple): Tupple of 2 integers corresponding to the axes streching
            along the spatial dimensions. Defaults to (1,2), 0 being the time axis

    Return:
        1D numpy array corresponding to spatially aggregated value for each time
            slice.

    Example:
        >>> import numpy as np

        >>> # 3D array with 23 time slices
        >>> array = np.random.rand(23, 3, 3)

        >>> # mask array. 1s are the locations under which we want to extract values
        >>> mask = np.array([[0,1,1],
        >>>                  [0,0,1],
        >>>                  [0,0,0]]) == 0

        >>> # Run the extraction
        >>> extract_from_mask(array, mask)
        >>> extract_from_mask(array, mask, 'sum')
    """
    mask_3d = np.broadcast_to(mask, array.shape)
    masked_array = np.ma.MaskedArray(array, mask_3d)
    if fun == 'mean':
        out = np.ma.mean(masked_array, axis=sp_axes)
    elif fun == 'median':
        out = np.ma.median(masked_array, axis=sp_axes)
    elif fun == 'min':
        out = np.ma.min(masked_array, axis=sp_axes)
    elif fun == 'max':
        out = np.ma.max(masked_array, axis=sp_axes)
    elif fun == 'sum':
        out = np.ma.sum(masked_array, axis=sp_axes)
    else:
        raise ValueError('fun= must be one of mean, median, min, max or sum')
    return out


def feature_transform(feature, crs_out, crs_in={'init': 'epsg:4326'}):
    """Reproject a dictionary representation of a feature in WGS84 to a desired projection

    Args:
        feature (dict): A dictionary representation of the feature (geojson like).
            coordinates must be in geographical coordinates, as per the geojson
            specifications. Supports feature types Point and Polygon
        crs (dict): A dictionary of projection parameters, or CRS object (see rasterio.crs module)

    Return:
        Dictionary representation of the input feature, projected to the desired CRS
    """
    p_in = Proj(crs_in)
    p_out = Proj(crs_out)
    feature_out = copy.deepcopy(feature)
    new_coords = []
    if feature['geometry']['type'] == 'Polygon':
        # Probably also work for multypolygons
        for ring in feature['geometry']['coordinates']:
            x2, y2 = transform(p_in, p_out, *zip(*ring))
            new_coords.append(zip(x2, y2))
        feature_out['geometry']['coordinates'] = new_coords
    elif feature['geometry']['type'] == 'Point':
        # Probably doesn't work for multipoints
        new_coords = transform(p_in, p_out, *feature['geometry']['coordinates'])
        feature_out['geometry']['coordinates'] = new_coords
    else:
        raise ValueError('Unsuported feature type')
    return feature_out
