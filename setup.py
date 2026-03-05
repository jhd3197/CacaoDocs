from setuptools import setup, find_packages
import pathlib

# Get the directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="cacaodocs",
    version='0.1.15',
    author="Juan Denis",
    author_email="juan@vene.co",
    description="Generate documentation from Python docstrings, powered by Cacao.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhd3197/CacaoDocs",
    packages=find_packages(exclude=["old", "old.*", "test-src", "test-docs"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires='>=3.10',
    install_requires=[
        "click>=8.0.0",
        "PyYAML>=6.0",
        "Markdown>=3.4",
        "cacao>=2.0.8",
    ],
    entry_points={
        'console_scripts': [
            'cacaodocs=cacaodocs.cli:main',
        ],
    },
)
