#!/usr/bin/env python

"""Connectome Mapping Toolkit
"""
from glob import glob
import os
import sys
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

packages=["cfflib"]

package_data = {'cfflib':
                ['schema/*.xsd',
                 ]}

################################################################################
# For some commands, use setuptools

if len(set(('develop', 'bdist_egg', 'bdist_rpm', 'bdist', 'bdist_dumb', 
            'bdist_wininst', 'install_egg_info', 'egg_info', 'easy_install',
            )).intersection(sys.argv)) > 0:
    from setup_egg import extra_setuptools_args

# extra_setuptools_args can be defined from the line above, but it can
# also be defined here because setup.py has been exec'ed from
# setup_egg.py.
if not 'extra_setuptools_args' in globals():
    extra_setuptools_args = dict()
    

def main(**extra_args):
    from distutils.core import setup
    
    setup(name='cfflib',
          version='0.9',
          description='Connectome File Format Library',
          long_description = """The Connectome File Format library supports easy handling of many neuroimaging formats and metadata for research in connectomics""",
          author='EPFL LTS5 Diffusion Group',
          author_email='info@connectomics.org',
          url='http://www.connectomics.org/',
          license='BSD License',
          packages = packages,
        classifiers = [c.strip() for c in """\
            Development Status :: 3 - Alpha
            Intended Audience :: Developers
            Intended Audience :: Science/Research
            Operating System :: OS Independent
            Programming Language :: Python
            Topic :: Scientific/Engineering
            Topic :: Software Development
            """.splitlines() if len(c.split()) > 0],    
          maintainer = 'Stephan Gerhard',
          maintainer_email = 'info@connectomics.org',
          package_data = package_data,
          **extra_args
         )

if __name__ == "__main__":
    main(**extra_setuptools_args)