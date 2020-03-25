import os
from setuptools import setup

long_description = open('README.md').read()

setup(
    name="mcd_changelog",
    version="0.2.0",
    description='parse mcd-changelog',
    long_description='Parse Maker\'s MCD changelog webpage',
    author="Jernej Mlakar",
    author_email="jernej.mlakar@gmail.com",
    url="N/A",
    license="https://unlicense.org/",
    packages=['mcd_changelog'],
    install_requires=['requests', 'beautifulsoup4'],
    keywords="maker makerDAO MCD mcd-changelog changelog",
    entry_points={'console_scripts': ['mcd_changelog=mcd_changelog.mcd_changelog:main',],},
    platforms="any"
)
