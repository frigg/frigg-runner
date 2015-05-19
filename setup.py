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
    'click==4.0',
    'invoke==0.10.1',
    'frigg-settings==1.0.0',
    'frigg-coverage==1.0.0',
]

test_requirements = [
    'pytest==2.7.1',
    'mock==1.0.1',
    'coverage==3.7.1',
    'six==1.9.0',
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
