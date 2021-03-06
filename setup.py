from setuptools import setup, find_packages

setup(author='Chris Rosenthal',
      author_email='crosenth@gmail.com',
      description='Interface to manipulate csv files as Pandas DataFrames.',
      name='csvpandas',
      packages=find_packages(exclude=['tests']),
      entry_points={'console_scripts': {'csvpandas = csvpandas:main'}},
      version='v0.0.7',
      url='https://github.com/crosenth/csvpandas',
      install_requires=['pandas>=0.17.1', 'xlrd>=0.9.0'],
      license='GPLv3',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Development Status :: 1 - Planning'
          ]
      )
