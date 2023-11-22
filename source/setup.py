"""
Creating compilild pyd libs
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("suppfun.pyx"),
)