from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cacaodocs",
    version="0.1.0",
    author="Juan Denis",
    author_email="juan@vene.co",
    description="A lightweight Python package to extract API documentation from docstrings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhd3197/CacaoDocs",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here
    ],
)
