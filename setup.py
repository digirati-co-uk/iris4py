#!/usr/bin/env python

from distutils.core import setup

setup(name='iris-core',
      version='0',
      description='Iris message bus',
      author='Digirati Ltd',
      packages=['iris',],
      license='MIT',
      install_requires=[
          'boto3'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python 3',
          'Programming Language :: Python 3 :: Only',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
      )
