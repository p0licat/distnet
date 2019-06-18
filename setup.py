from setuptools import setup, find_packages
from pkg_resources import resource_filename
# import pkg_resources


__version__ = '0.1.52'

versionFile = resource_filename(__name__, 'distnet/resources/VERSION')

with open(versionFile, 'w') as fd:
    fd.write(__version__)
    fd.close()

setup(
    name='distnet',
    version=__version__,
    author='p0licat',
    author_email='tbodica@gmail.com',
    install_requires=[
        'pygal_maps_world',
        'pygame',
        'python-whois', #TODO: check for whois package, conflicting?
        'cairosvg',
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
)
