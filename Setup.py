from setuptools import setup, find_packages
 
import pySolanio
 
setup(
 
    name='pySolanio',
    
    version=pySolanio.__version__,

    packages=find_packages(),
 
    author="Linard Y.",

    author_email="yldev@free.fr",
 
    description="Solution analysis input/output",

    long_description=open('README.md').read(),
 
    include_package_data=True,

    url='http://github.com/linard-y/pySolanio',
 
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Chemical Data Manipulation",
    ]
 
)
