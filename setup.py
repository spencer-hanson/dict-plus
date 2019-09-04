from setuptools import setup


def parse_requirements(requirement_file):
    return ""
    # Code doesn't work with python2.7 installation, just return the requirement hardcoded
    # with open(requirement_file) as fi:
    #     return fi.readlines()


with open('./README.rst') as f:
    long_description = f.read()

setup(
    name='dict_plus',
    packages=['dict_plus'],
    version='0.1.1',
    description='Extended Dictionary Package',
    author='Spencer Hanson',
    author_email="spencerhanson3141@gmail.com",
    long_description=long_description,
    install_requires=parse_requirements('requirements.txt'),
    keywords=['list', 'utilities', 'dictionary'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]
)
