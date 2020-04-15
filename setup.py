import os
from setuptools import setup

setup(
    name="mcd_changelog",
    version="0.4.3",
    description='parse mcd-changelog (BETA)',
    long_description='Parse Maker\'s MCD changelog webpage',
    author="Jernej Mlakar",
    author_email="jernej.mlakar@gmail.com",
    url="https://github.com/jernejml/mcd_changelog",
    license="https://unlicense.org/",
    packages=['mcd_changelog'],
    install_requires=['requests', 'beautifulsoup4'],
    keywords="maker makerDAO MCD mcd-changelog changelog",
    entry_points={'console_scripts': ['mcd_changelog=mcd_changelog.mcd_changelog:main',],},
    platforms="any"
)
