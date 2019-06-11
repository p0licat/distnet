from setuptools import setup, find_packages
from pkg_resources import resource_filename
# import pkg_resources


__version__ = '0.1.4404'
#
# import distnet
# # Could be any dot-separated package/module name or a "Requirement"
# resource_package = distnet.__name__
# resource_path = '/'.join(('resources', 'VERSION'))  # Do not use os.path.join()
# template = pkg_resources.resource_filename(resource_package, resource_path)


template = resource_filename(__name__, 'distnet/resources/VERSION')
print(template)

with open(template, 'w') as fd:
    fd.write(__version__)
    fd.close()

setup(
    name='distnet',
    version=__version__,
    author='pawel',
    author_email='pawel@local.host',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
)
