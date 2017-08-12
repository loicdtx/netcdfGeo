from setuptools import setup, find_packages

setup(name='netcdfGeo',
      version='0.0.1a',
      description='Gdal compliant handling of projected spatio-temporal data in NetCDF',
      long_description='TODO',
      classifiers=[],
      keywords='netcdf spatial temporal gdal',
      author='Loic Dutrieux',
      author_email='loic.dutrieux@gmail.com',
      url='https://github.com/loicdtx/netcdf-geo',
      license='GPLv3',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'rasterio==1.0a9',
          'numpy',
          'netCDF4',
          'pyproj',
          'affine'],
      test_suite='tests')


