#!/usr/bin/env python

from setuptools import setup

setup(name='textme',
      version='0.1.1a1',
      description='Command-line tool for sending SMS',
      long_description="""textme is a command-line tool for sending SMS using
      the 46elks platfrom from the terminal.""",
      url="https://github.com/46elks/textme",
      author="Emil Tullstedt",
      author_email='emil@46elks.com',
      license='MIT',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
#        'Programming Language :: Python :: 3',
#        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Monitoring'
      ],
      keywords="sms 46elks cli monitoring",
      use_2to3 = True)

