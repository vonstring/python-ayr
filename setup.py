#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='python-ayr',
    version='0.0.1',
    description='Asynchronously get the forecast from the norwegian weather service yr.no in python',
    long_description=open('README.rst').read(),
    author='Kristian von Streng Haehre',
    author_email='kristian.vsh@gmail.com',
    url='https://github.com/vonstring/python-ayr',
    packages=['ayr'],
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet',
    ],
    package_data={
        'ayr': [
            'languages/*.json',
        ],
    },
    install_requires=['xmltodict', 'aiohttp'],  # $$solve$$ ~> /usr/lib/python3.4/distutils/dist.py:260: UserWarning: Unknown distribution option: 'install_requires' warnings.warn(msg)
)
