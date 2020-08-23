## Copyright (c) 2020 mangalbhaskar.
"""setup script."""
__author__ = 'skillplot'
__version__ = '1.0.7'

_name_ = 'pyboozo' 

import setuptools


from os import path
## read the contents of your README file
## https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setuptools.setup(
  name = _name_
  ,version = __version__
  ,description = 'An opinionated software development environment setup and configuration generator.'
  ,long_description = long_description
  ,long_description_content_type = 'text/markdown; charset=UTF-8; variant=GFM'
  # ,license='Apache 2.0'
  ,packages=setuptools.find_packages()
  ,python_requires='~=3.6'
  ,author = __author__
  ,author_email='skillplot@gmail.com'
  ,url = 'https://github.com/{}/{}'.format(__author__, _name_)
  ,project_urls={
      'Download': 'https://github.com/{}/{}/archive/{}.tar.gz'.format(__author__, _name_, __version__)
  }
  ,keywords = ['software development', 'configuration generator', 'environment setup']
  ,install_requires=[
    'easydict'
    ,'PyYaml'
    ,'arrow'
    ,'click'
  ]
  ,include_package_data=True
  ,package_data={
    "data": ["*"] ### And include any *. files found in the "data" package:
  }
  ,data_files=[
    ('',['boozo/data/gitignore']),
  ]
  ,entry_points={
    'console_scripts':[
      'boozo=boozo.__main__:main'
    ]
    ,'gui_scripts':[]
  }
  ,classifiers=[
    'Development Status :: 5 - Production/Stable'      # Chose either '3 - Alpha', '4 - Beta' or '5 - Production/Stable' as the current state of your package
    ,'Intended Audience :: Developers'
    ,'Topic :: Software Development :: Build Tools'
    ,'License :: OSI Approved :: Apache Software License'  
    ,'Operating System :: POSIX :: Linux'
    ,'Programming Language :: Python :: 3'
    ,'Programming Language :: Python :: 3.6'
    ,'Environment :: Console'
  ],
)