# all .pyx files in a folder
from distutils.core import setup
from Cython.Distutils import build_ext
import setuptools
from setuptools import Extension

cmdclass = {}
ext_modules = [Extension("indicators", ["src/indicators.pyx"])]
cmdclass.update({'build_ext': build_ext})

setuptools.setup(
    name="epociask", # Replace with your own username
    version="0.1.0",
    author="Ethen Pociask",
    author_email="epociask@volatrade.com",
    description="Indicator functions using cython",
    long_description="TO BE ADDED",
    long_description_content_type="text/markdown",
    url="https://github.com/epociask/cython_indicator_functions.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass = cmdclass,
    ext_modules = ext_modules,

)

