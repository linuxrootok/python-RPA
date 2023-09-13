from setuptools import setup, find_packages
import os

setup(
    name='myrpa',
    version='0.1',
    packages=find_packages(),
    scripts=['bin/my_command.py'],
    entry_points={
        'console_scripts': [
            'syncProjects = bin.my_command:getData'
        ]
    }
)