# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Dojotools',
    version='1.0',
    packages=find_packages(),
    scripts=['dojotools'],
    install_requireses=[
        'pyserial',
        'pygtk',
    ],
    author="Flávio Amieiro",
    author_email="amieiro.flavio@gmail.com",
    long_description="Dojotools is intended to help in coding dojo sessions. Our huge feature list is: watch a directory for changes and run a user supplied command when a file changes and keep track of the round time (in the simplest way possible)",
    license="GPL",
    keywords="dojo python",
    url="http://www.github.com/flavioamieiro/dojotools"
)
