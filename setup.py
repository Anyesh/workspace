from setuptools import find_packages, setup


def read_file(name):
    with open(name) as fd:
        return fd.read()


setup(
    name="workplace",
    version="0.1.0",
    description=("my workspace"),
    author="Anish Shrestha",
    author_email="connect@anyesh.me",
    packages=find_packages(exclude=["tests"]),
    install_requires=read_file("requirements.txt").splitlines(),
    entry_points={
        "console_scripts": ["workplace=run:cli"],
    },
    package_data={"": ["config.yaml", "README.md"]},
    include_package_data=True,
    zip_safe=False,
)