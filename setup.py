from setuptools import setup


def parse_requirements(requirement_file):
    with open(requirement_file) as fi:
        return fi.readlines()


with open('./README.rst') as f:
    long_description = f.read()

setup(
    name='dict_plus',
    packages=['dict_plus'],
    version='0.0.4',
    description='Extended Dictionary Package',
    author='Spencer Hanson',
    author_email="spencerhanson3141@gmail.com",
    long_description=long_description,
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['list', 'utilities', 'dictionary'],
    classifiers=[],
)