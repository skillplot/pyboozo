## Copyright (c) 2020 mangalbhaskar
"""Common File I/O utilities.

Dependencies: easydict, pandas, yaml
"""
__author__ = 'mangalbhaskar'


import errno
import logging
import os
import json
import pathlib
import sys
import time

from easydict import EasyDict as edict
import yaml

from boozo.boot._log_ import log
#log = logging.getLogger('__main__.'+__name__)

this = sys.modules[__name__]


def load_file(filepath, withedict=True):
  """Safe load file as easy dictionary object by default.
  Currently, `yml`, `json`, `csv` files are supported."""
  fc = None
  if str == type(filepath) and os.path.exists(filepath) and os.path.isfile(filepath):
    ext = os.path.splitext(filepath)[-1].split('.')[-1]
    log.debug("ext, type(ext): {}, {}".format(ext, type(ext)))
    fn = getattr(this, ext+'_load') 
    fc = fn(filepath, withedict)
  else:
    log.exception("Invalid filepath: {}".format(filepath), exc_info=True)
  return fc


def yml_load(filepath, withedict=True):
  """Safe load yaml file as easy dictionary object."""
  fc = None
  tic = time.time()
  log.debug("filepath, type(filepath): {}, {}".format(filepath, type(filepath)))
  with open(filepath, 'r') as f:
    if withedict:
      ## fc = edict(yaml.load(f))
      fc = edict(yaml.safe_load(f))
    else:
      fc = yaml.safe_load(f)
    log.debug('Done (t={:0.2f}s)'.format(time.time()- tic))
  return fc


def json_load(filepath, withedict=True):
  """Load json file as easy dictionary object."""
  fc = None
  tic = time.time()
  with open(filepath, 'r') as f:
    if withedict:
      fc = edict(json.load(f))
    else:
      fc = json.load(f)
    log.info('Done (t={:0.2f}s)'.format(time.time()- tic))
  return fc


def csv_load(filepath, withedict=True):
  """Load csv file as easy dictionary object."""
  import pandas as pd
  if withedict:
    fc = edict(pd.read_csv(filepath))
  else:
    fc = pd.read_csv(filepath)
  return fc


def read_csv_line(filepath, delimiter = ','):
  """Read CSV Line as a generator for large csv files."""
  with open(filepath, 'r') as f:
    gen = (i for i in f)
    ## next(gen)
    yield next(gen).rstrip('\n').split(delimiter)
    for line in gen:
      yield line.rstrip('\n').split(delimiter)


def yml_safe_dump(filepath, o, default_flow_style=False):
  """Create yaml file from python dictionary object."""
  with open(filepath,'w') as f:
    yaml.safe_dump(o, f, default_flow_style=default_flow_style)


def json_dump(filepath, o):
  """Create json file from python dictionary object."""
  tic = time.time()
  with open(filepath,'w') as f:
    f.write(json.dumps(o))
    log.info('Done (t={:0.2f}s)'.format(time.time()- tic))

def list_files(p, ext=None):
  """List files in a given path."""
  pattern = r'**/*.{}'.format(ext) if ext else r'**/*'
  for f in pathlib.Path(p).glob(pattern):
    if os.path.isfile(f):
     yield f.as_posix()


def get_filelist(basepath, exts=[]):
  """Returns the filtered list of files based on the given list of extensions.

  Args:
    basepath (string): basepath directory to scan
    exts (list, optional): list of file extensions with dot.
                @Example: ['.jpg','.png']
  """
  filelist = []
  for f in os.listdir(basepath):
    if f.is_file():
      if exts and len(exts) > 0:
        if os.path.splitext(f.name)[-1].lower() in exts:
          filelist.append(f.path)
      else:
        filelist.append(f.path)
  return filelist


def get_only_files_in_dir(path):
  """returns file in a director as a generator
  Usage: list( get_only_files_in_dir(path) )
  """
  for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)):
      yield os.path.join(path, file)


def list_dirs(p):
  """List directories in a given path."""
  for f in pathlib.Path(p).glob(r'**/*'):
    if os.path.isdir(f):
     yield f.as_posix()


def mkdir_p(p):
  """mkdir -p` linux command functionality.

  References:
  * https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
  * https://stackoverflow.com/questions/20794/find-broken-symlinks-with-python
  """
  try:
    os.makedirs(p)
  except OSError as exc:  ## Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(p):
      pass
    elif os.path.islink(p) and not os.path.exists(p):
      os.remove(p)
      mkdir_p(p)
    else:
      raise
