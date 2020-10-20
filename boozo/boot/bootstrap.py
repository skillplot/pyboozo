## Copyright (c) 2020 mangalbhaskar.
"""Utility functions to bootstrap the application."""
__author__ = 'mangalbhaskar'

__all__ = [
  'generate_exportsh'
  ,'generate_aliassh'
  ,'generate_envsh'
  ,'generate_cfgyml'
  ,'make_dirs'
  ,'make_links'
]


import os
import pathlib
import sys

from ._log_ import log

from boozo.utils import fio
from boozo.utils import common
from boozo.utils import timestamp
from boozo.utils import recurse
from boozo.utils.typeformats import *


def generate_exportsh(**kwargs):
  """Generate the `{}.env.sh` in the config directory."""
  filepath = os.path.join(kwargs['_CONFIG'], "{}.export.sh".format(kwargs['_NAME']))
  log.info("HOME:{}\nfilepath: {}".format(kwargs['_NAME'], filepath))
  with open(filepath, 'w') as f:
    f.write('{}\n'.format(_shebang_))
    f.write('## {}\n'.format(_copyright_))
    f.write('## {}\n'.format(_banner_))
    f.write('source $( cd "$( dirname "${}")" && pwd )/{}\n'.format('{BASH_SOURCE[0]}', '{}.export.sh'.format(kwargs['_NAME'])))
    f.write('source $( cd "$( dirname "${}")" && pwd )/{}\n'.format('{BASH_SOURCE[0]}', '{}.alias.sh'.format(kwargs['_NAME'])))
  return filepath


def generate_aliassh(**kwargs):
  """Generate the `{}.alias.sh` in the config directory."""
  filepath = os.path.join(kwargs['_CONFIG'], "{}.alias.sh".format(kwargs['_NAME']))
  log.info("HOME:{}\nfilepath: {}".format(kwargs['_NAME'], filepath))
  with open(filepath, 'w') as f:
    f.write('{}\n'.format(_shebang_))
    f.write('## {}\n'.format(_copyright_))
    f.write('## {}\n'.format(_banner_))
    for K,V in kwargs['_ALIAS'].items():
      f.write('alias {}={}\n'.format(K.replace('_','').lower(), V))
  return filepath


def generate_envsh(**kwargs):
  """Generate the `{}.export.sh` in the config directory.

  References:
  * https://stackoverflow.com/questions/5564418/exporting-an-array-in-bash-script
  """
  filepath = os.path.join(kwargs['_CONFIG'], "{}.env".format(kwargs['_NAME']))
  log.debug("HOME: {}\nfilepath: {}".format(kwargs['_NAME'], filepath))
  with open(filepath, 'w') as f:
    f.write('{}\n'.format(_shebang_))
    f.write('## {}\n'.format(_copyright_))
    f.write('## {}\n'.format(_banner_))
    for K,V in recurse.get_from_dict(kwargs['_ENVCFG'], kwargs['_VAR'].split(":")):
      if type(V) == list or type(V) == tuple:
        # V = '<('+common.list_to_str(V, dl=' ', quote=True)+')'
        V = common.list_to_str(V, dl=':')
      if V == None:
        V = ''
      f.write('export {}="{}"\n'.format(K, V))
  return filepath


def generate_cfgyml(**kwargs):
  """Generated the `{}.yml` in the config directory."""
  filepath = os.path.join(kwargs['_CONFIG'], "{}.yml".format(kwargs['_NAME']))
  log.debug("HOME: {}\nfilepath: {}".format(kwargs['_NAME'], filepath))
  fio.yml_safe_dump(filepath, kwargs['_ENVCFG'])
  return filepath


def make_dirs(*args, gitkeep=False):
  """Create directories."""
  for p in args:
    if p:
      _p = pathlib.Path(p)
      log.debug("make_dirs:_p: {}".format(_p))
      fio.mkdir_p(_p)
      ## Creates a an empty file for git
      if gitkeep:
        with open(os.path.join(_p, '.gitkeep'), 'w') as f:
          pass

def _create_link_(l, newpath=None):
  """Create the link based on path and optional newpath"""
  _l = pathlib.Path(l)
  # log.debug("make_links:_l:{}, newpath: {}".format(_l, newpath))
  if _l.is_symlink():
    pass
  else:
    if _l.is_dir():
      if newpath is None:
        newpath = _l.joinpath(_l.parent, '.'+_l.name+'-'+timestamp.ts())
      # log.debug("oldpath: {} and newpath: {}".format(_l, newpath))
      # log.debug("os.path.basename(newpath): {}".format(os.path.basename(newpath)))
      _l.rename(newpath)
      _l.symlink_to(os.path.basename(newpath))
    else:
      # log.debug("oldpath: {} and newpath: {}".format(_l, newpath))
      _l.symlink_to(newpath)


def make_links(*args, **kwargs):
  """Make symlinks."""
  ## timestamp based newpath
  if args is not None and len(args) > 0:
    for l in args:
      _create_link_(l)
  ## key is the oldpath, value is the newpath
  if kwargs is not None and len(kwargs) > 0:
    for kl,vl in kwargs.items():
      _create_link_(kl, vl)
