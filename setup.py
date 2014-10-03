#!/usr/bin/env python

from setuptools import setup, find_packages

import os

requires = [
    'boto==2.32.1',
    'requests==2.4.1',
    'click==2.4']

setup(
    name='heartbeat',
    version=open(os.path.join('skew', '_version')).read(),
    description='Send a heartbeat custom metric to StackDriver',
    author='Mitch Garnaat',
    author_email='mitch@scopely.com',
    url='https://github.com/scopely-devops/heartbeat',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],
    platforms=['Any'],
    scripts=['bin/heartbeat'],
    packages=find_packages(),
)
