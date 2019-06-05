from setuptools import setup, find_packages

__version__ = '0.1.42'

with open('distnet/VERSION', 'w') as fd:
    fd.write(__version__)
    fd.close()

setup(
    name='distnet',
    version=__version__,
    author='pawel',
    author_email='pawel@local.host',
    packages=find_packages(exclude=['tests']),
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
)
