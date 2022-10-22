from setuptools import setup

setup(
   name='pyoshub',
   version='0.4.0',
   author='Klaus G. Paul',
   author_email='20340525+KlausGPaul@users.noreply.github.com ',
   packages=['pyoshub', 'pyoshub.test'],
   scripts=[],
   url='http://pypi.python.org/pypi/pyoshub/',
   license='LICENSE.txt',
   description='API scripts to access https://opensupplyhub.org Open Supply Hub\'s API',
   long_description=open('README.rst').read(),
   install_requires=[
       "requests",
       "pytest",
       "pyyaml",
   ],
)