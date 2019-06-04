from setuptools import setup, find_packages

setup(
    name='distnet',
    version='0.1.41',
    author='pawel',
    author_email='pawel@local.host',
    packages=find_packages(exclude=['tests']),
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
)
