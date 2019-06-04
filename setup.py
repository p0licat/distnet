from setuptools import setup, find_packages

setup(
    name='distnet',
    version='0.1.4',
    author='pawel',
    author_email='pawel@local.host',
    packages=find_packages(exclude=['tests']),
    scripts=['test_entry_point.py'], # TODO: scripts and src restructure
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
)
