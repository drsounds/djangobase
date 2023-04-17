#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


from djangobase import __version__


setup(
    name='djangobase',
    version=__version__,
    description='A Firebase like Django API.',
    author='Alexander Forselius',
    author_email='drsounds@gmail.com',
    url='https://github.com/Buddhalow/djangobase',
    long_description=open('README.rst', 'r').read(),
    packages=[
        'djangobase'
    ],
    package_data={
        'djangobase': ['templates/djangobase/*'],
    },
    zip_safe=False,
    requires=[
        'python_mimeparse(>=0.1.4, !=1.5)',
        'dateutil(>=2.1)',
    ],
    install_requires=[
        'python-mimeparse >= 0.1.4, != 1.5',
        'python-dateutil >= 2.1',
    ],
    tests_require=['PyYAML', 'lxml', 'defusedxml'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
)