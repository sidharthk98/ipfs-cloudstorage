from setuptools import setup, find_packages

import sys
print("__file__:", __file__)
print("sys.path:", sys.path)

setup(
    name='ipfs',
    version='1.3',
    packages=['ipfs'],
    install_requires=['subprocess.run','ipfshttpclient','google-cloud-storage','argparse','tinydb','fnmatch2'],
    entry_points={
        'console_scripts': [
            'osis = ipfs.cli:main',  # This defines the CLI entry point
        ],
    },
)
