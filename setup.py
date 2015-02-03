#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'invoke',
    'pyaml',
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-sugar',
    'mock'
]

setup(
    name='frigg-runner',
    version='0.0.1',
    description="Frigg runner execute .frigg.yml file localy.",
    long_description=readme + '\n\n' + history,
    author="Eirik Martiniussen Sylliaas",
    author_email='eirik@sylliaas.no',
    url='https://github.com/eirsyl/frigg-runner',
    packages=find_packages(exclude='tests'),
    package_dir={'frigg-runner':
                 'frigg-runner'},
    include_package_data=True,
    entry_points={
        "console_scripts": ['frigg = frigg_runner.cli:main']
    },
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='frigg-runner',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
