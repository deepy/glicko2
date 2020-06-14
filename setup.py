import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="glicko2",
    version="2.0.0",
    author="Alexander Nordlund",
    author_email="deep.alexander@gmail.com",
    description="Python implementation of glicko2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepy/glicko2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)