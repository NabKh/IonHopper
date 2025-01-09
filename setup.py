from setuptools import setup, find_packages

setup(
    name="bhmc-vasp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ase>=3.22.1",
        "numpy>=1.21.0",
        "pyyaml>=5.4.1"
    ],
    author="Your Name",
    description="Basin Hopping Monte Carlo for VASP",
    python_requires=">=3.8",
)
