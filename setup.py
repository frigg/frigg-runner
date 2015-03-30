#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from frigg_runner import __version__

try:
    with open('README.rst') as readme_file:
        readme = readme_file.read()
except:
    readme = ''


requirements = [
    'click==3.3',
    'invoke==0.10.1',
    'frigg-common==0.2.0',
    'frigg-coverage==0.5.0',
    'clint==0.4.1',
]

test_requirements = [
    'pytest==2.7.0',
    'mock==1.0.1',
    'coverage==3.7.1',
]

setup(
    name='frigg-runner',
    version=__version__,
    description="Frigg runner execute .frigg.yml file localy.",
    long_description=readme,
    author="Eirik Martiniussen Sylliaas",
    author_email='eirik@sylliaas.no',
    maintainer='The frigg team',
    maintainer_email='hi@frigg.io',
    url='https://github.com/frigg/frigg-runner',
    packages=find_packages(),
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
