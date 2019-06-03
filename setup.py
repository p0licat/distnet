from distutils.core import setup

setup(
    name='distnet',
    version='0.1.0',
    author='pawel',
    author_email='pawel@local.host',
    packages=['src'],
    scripts=[''], # TODO: scripts and src restructure
    url='http://pypi.python.org/pypi/none',
    license='LICENSE.txt',
    description='Linux networking tools in python.',
    long_description=open('README.txt').read(),
    #install_requires=[
    #],
)
