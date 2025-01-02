from setuptools import setup, find_packages
import pathlib

# Get the directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="cacaodocs",
    version="0.1.3",
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
        "Jinja2==3.0.0",
        "Markdown==3.7",
        "beautifulsoup4==4.12.3",
        "Flask==2.0.0",
        "PyYAML==6.0.2",
        "Werkzeug==2.0.0",
        "Flask-Cors==5.0.0",
    ],
    include_package_data=True,
)
