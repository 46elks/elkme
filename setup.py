#!/usr/bin/env python

from setuptools import setup, find_packages
from elkme.__init__ import __version__

setup(name='elkme',
      version=__version__,
      description='Command-line tool and SDK for sending SMS',
      long_description="""elkme is a command-line tool for sending SMS using
      the 46elks platfrom from the terminal which doubles as an SDK to use
      when building applications utilizing the 46elks platform""",
      url="https://github.com/46elks/elkme",
      author="Emil Tullstedt",
      author_email='emil@46elks.com',
      license='MIT',
      packages = find_packages(),
      install_requires = ['requests>=2.10.0'],
      tests_require = ['nose>=1.3.7'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Monitoring'
      ],
      keywords="sms 46elks cli monitoring",
      entry_points={
            'console_scripts': [
                'elkme = elkme.main:main'
                ]
          },
      use_2to3 = False,
      test_suite = 'nose.collector')

