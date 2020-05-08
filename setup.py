# Time-stamp: <Thu 2018-11-29 14:58 svarrette>

"""PRESENCE: Monitoring and Modelling the Performance Metrics of Mobile Cloud SaaS Web Services

Setuptools configuration file.

Resources:
- https://packaging.python.org/en/latest/distributing/
- https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
- https://github.com/jeffknupp/sandman2
"""

from __future__ import print_function

# Preliminary checks that cannot be done by setuptools
# like... the setuptools dependency itself!
# Thanks [Serge and Pythran](https://github.com/serge-sans-paille/pythran) for suggesting that ;)
try:
    import setuptools
except ImportError:
    print()
    print("*****************************************************")
    print("* Setuptools must be installed before running setup *")
    print("*****************************************************")
    print()
    raise

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

LONG_DESCRIPTION = read('README.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--strict',
            '--verbose',
            '--tb=long',
            'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='presence',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=find_version('presence', '__init__.py'),
    license='Apache Software License',

    # The project's main homepage and description
    url='https://gitlab.uni.lu/aibrahim/presence',
    description='Novel Prototype for Monitoring and Modelling the Performance Metrics of Mobile Cloud SaaS Web Services',
    long_description=LONG_DESCRIPTION,

    # Author details
    author='A. A.Z.A Ibrahim, S. Varrette',
    author_email='abdallah.ibrahim@uni.lu',

    #
    tests_require=['pytest', 'pytest-cov', 'pytest-flask>=0.4.0'],

    # Run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Flask>=0.10.1',
        'Flask-SQLAlchemy>=1.0',
        'SQLAlchemy==1.2.12',
        'Flask-Admin>=1.0.9',
        'Flask-HTTPAuth>=3.1.2',
    ],
    cmdclass={'test': PyTest},

    packages=find_packages(),
    include_package_data=True,

    platforms='any',
    test_suite='tests.test_presence',
    zip_safe=False,

    #package_data={'presence': ['templates/**.yaml']},

    # List of classifiers the categorize your project.
    # For a full listing, see https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        # How mature is the project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved',
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Environment :: Console',
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points='''
        [console_scripts]
        presence=presence.presence:presence
    ''',

)
