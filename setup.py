import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open(HERE / "requirements.txt") as f:
    required_packages = f.read().splitlines()

README = (HERE / "README.md").read_text()
VERSION = (HERE / ".version").read_text()

setup(
    name="prefectplayground",
    version=VERSION,
    description="Prefect Playground",
    author="D. Severin Ryberg",
    author_email="severin-ryberg@sevberg.dev",
    packages=["prefectplayground"],
    install_requires=required_packages,
)
