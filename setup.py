from __future__ import print_function 
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages 
import io
import codecs
import os
import sys
import subprocess 
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CHANGES.md')


VERSION_PY = """
# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.

__version__ = '%s'
"""

def update_version_py():
    
    if not os.path.isdir(".git"):
        print("This does not appear to be a Git repository.")
        return
    try:
        p = subprocess.Popen(
            ["git", "describe", "--tags", "--dirty", "--always"],
            stdout=subprocess.PIPE)
    except EnvironmentError:
        print("unable to run git, leaving pie/_version.py alone")
        return
    stdout = p.communicate()[0]
    if p.returncode != 0:
        print("unable to run git, leaving pie/_version.py alone")
        return
    ver = "1.0+" + stdout.strip()
    if ver.find("-dirty") > -1:
        print(sys.stderr, "REFUSING TO INSTALL DIRTY TREE! COMMIT TO TRUNK OR BRANCH!")
        #sys.exit(1)
    f = open("pie/_version.py", "w")
    f.write(VERSION_PY % ver)
    f.close()
    print("set pie/_version.py to '%s'" % ver)


def get_version():
    try:
        f = open("cmo/_version.py")
    except EnvironmentError:
        return None
    for line in f.readlines():
        mo = re.match("__version__ = '([^']+)'", line)
        if mo:
            ver = mo.group(1)
            return ver
    return None



setup(
    name='pie',
    version=get_version(),
    description=
    'Precision Informatics Engine, Python Package',
    url='github.com/rhshah/pie.git',
    author='Ronak Shah',
    author_email='rons.shah@gmail.com',
    licence='Apache License, Version 2.0',
    packages=find_packages(),
    dependency_links=[
    ],
    install_requires=[
        'argparse',
        'filemagic',
        'coloredlogs'
    ],
    scripts=[
        'bin/pie_bwa_mem.py',
        'bin/pie_cutadapt.py',
        'bin/pie_mutect.py',
        'bin/pie_picard_markduplicates.py',
        'bin/pie_vardict.py'
    ],
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Development Status :: 3'
        ),
    )
