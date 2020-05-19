import os
import sys
from shutil import rmtree

from setuptools import setup, find_packages, Command


here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'river', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


# Adapted from: https://github.com/navdeep-G/setup.py/blob/master/setup.py
# (Public domain software)
class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
                  sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/* '
                  '--repository-url http://pypi.neighborhoods.com/simple/')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about["__version__"]))
        os.system('git push --tags')

        sys.exit()


setup(
    name=about['__title__'],
    url=about['__url__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.10.0'
        'pandas>=1.0.0'
    ]
 )