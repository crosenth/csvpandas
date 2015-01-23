import subprocess

from setuptools import setup, find_packages

try:
    subprocess.check_call(
        'git describe --tags --long > csvpandas/data/version',
        shell=True)
except subprocess.CalledProcessError:
    version = ''
else:
    with open('csvpandas/data/version') as f:
        version = f.read().strip().split('-')[0]

setup(author='Chris Rosenthal',
      author_email='crosenth@gmail.com',
      description='',
      name='csvpandas',
      packages=find_packages(exclude=['tests']),
      entry_points={'console_scripts': {'csvpandas = csvpandas:main'}},
      version=version,
      url='https://github.com/crosenth/csvpandas',
      requires=['python (>= 2.7.5)'],
      install_requires=['pandas==0.15.2'])
