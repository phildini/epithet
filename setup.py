#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyGithub==1.34',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='epithet',
    version='0.0.3',
    description="Manage your labels.",
    long_description=readme + '\n\n' + history,
    author="Philip James",
    author_email='phildini@phildini.net',
    url='https://github.com/phildini/epithet',
    packages=[
        'epithet',
    ],
    package_dir={'epithet':
                 'epithet'},
    entry_points={
        'console_scripts': [
            'epithet=epithet.epithet:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='epithet',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
