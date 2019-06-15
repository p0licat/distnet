from setuptools import setup, find_packages
from pkg_resources import resource_filename
# import pkg_resources


__version__ = '0.1.4406'

versionFile = resource_filename(__name__, 'distnet/resources/VERSION')

with open(versionFile, 'w') as fd:
    fd.write(__version__)
    fd.close()

setup(
    name='distnet',
    version=__version__,
    author='pawel',
    author_email='pawel@local.host',
    install_requires=[
        'pygal_maps_world',
        'pygame',
        #'pygal_maps_world',
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
)
