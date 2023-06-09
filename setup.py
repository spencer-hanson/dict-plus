from setuptools import setup
import json

VERSION = "0.3.3"


def check_version_info():
    try:
        with open("version.json", "r") as f:
            data = json.load(f)
            assert data["version"] == VERSION  # Assert that the versions are the same
    except IOError:
        # File doesn't exist, ignore
        return


def parse_requirements(requirement_file):
    return ""
    # Code doesn't work with python2.7 installation, just return the requirement hardcoded
    # with open(requirement_file) as fi:
    #     return fi.readlines()


with open('./README.rst') as f:
    long_description = f.read()

check_version_info()

setup(
    name='dict_plus',
    packages=['dict_plus', 'dict_plus.dicts', 'dict_plus.indexes', 'dict_plus.lists', 'dict_plus.elements'],
    version=VERSION,
    description='Extended Dictionary Package',
    author='Spencer Hanson',
    author_email="spencerhanson3141@gmail.com",
    long_description=long_description,
    install_requires=parse_requirements('requirements.txt'),
    keywords=['list', 'utilities', 'dictionary'],
    # classifiers=[
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3'
    # ]
)
