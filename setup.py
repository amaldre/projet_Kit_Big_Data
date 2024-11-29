from setuptools import setup, find_packages

setup(
    name='projet_big_data',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
