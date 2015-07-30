#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='elkme',
      version='0.3.0',
      description='Command-line tool for sending SMS',
      long_description="""elkme is a command-line tool for sending SMS using
      the 46elks platfrom from the terminal.""",
      url="https://github.com/46elks/elkme",
      author="Emil Tullstedt",
      author_email='emil@46elks.com',
      license='MIT',
      packages = find_packages(),
      packages_dir = {'': 'elkme'},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Monitoring'
      ],
      keywords="sms 46elks cli monitoring",
      entry_points={
            'console_scripts': [
                'textme = elkme.main:main',
                'elkme = elkme.main:main'
                ]
          },
      use_2to3 = False)

