import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="glicko2",
    version="2.1.0",
    author="Alexander Nordlund",
    author_email="deep.alexander@gmail.com",
    description="Python implementation of glicko2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepy/glicko2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 6 - Mature",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires='>=3.7',
)
