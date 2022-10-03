from setuptools import find_packages, setup


def read_file(name):
    with open(name) as fd:
        return fd.read()


setup(
    name="workspace",
    version="0.1.0",
    description=("my workspace"),
    author="Anish Shrestha",
    author_email="connect@anyesh.me",
    packages=find_packages(exclude=["tests"]),
    install_requires=read_file("requirements.txt").splitlines(),
    entry_points={
        "console_scripts": ["ws=workspace.cli"],
    },
    package_data={"": ["README.md"]},
    include_package_data=True,
    zip_safe=False,
)
