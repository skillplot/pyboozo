## Copyright (c) 2020 mangalbhaskar
"""Caution: recursive utility functions."""
__author__ = 'mangalbhaskar'

import os


def dict_keys_to_lowercase(d):
  """Converts all the dictionary keys to lowercase in
  recursive function call.
  """
  d_mod = { k.lower():d[k] if not isinstance(d[k],dict) else dict_keys_to_lowercase(d[k]) for k in d.keys() }
  return d_mod


def get_from_dict(dictionary, keys=None):
  """recursive generator to fetch the non-dict values in the nested dictory.

  References:
  * https://stackoverflow.com/questions/38254304/can-generators-be-recursive
  """
  if not keys:
    keys = list(dictionary.keys())
  for val in keys:
    vval = dictionary[val]
    if type(vval) != dict:
      yield val, vval
    if type(vval) == dict:
      yield from get_from_dict(vval)


def get_basepath(p):
  """Ensures the last Directory of a path in a consistent ways.
  basepath is returned for a file or path. It takes care of
  trailing slash for a file or a directory.
  """
  if os.path.isdir(p):
    base_path = os.path.join(p,'')
  else:
    base_path = os.path.join(os.path.dirname(p),'')
  _bp = base_path.rstrip(os.path.sep)
  if os.path.isfile(_bp):
    _bp = get_basepath(_bp)
  return _bp


def scandir(basepath, exts=[]):
  """Scan a directory re-currsively and returns the list of sub-folders and files in the given directory,
  given the list of extension.

  Reference:
  `Adapted from https://stackoverflow.com/a/59803793 credit: https://stackoverflow.com/users/2441026/user136036`

  Args:
    basepath (string): basepath directory to scan
    exts (list, optional): list of file extensions with dot.
                @Example: ['.jpg','.png']
  """
  subfolders, filelist = [], []
  for f in os.scandir(basepath):
    if f.is_dir():
      subfolders.append(f.path)
    if f.is_file():
      if len(exts) > 0:
        if os.path.splitext(f.name)[1].lower() in exts:
          filelist.append(f.path)
          filelist.append()
      else:
        filelist.append(f.path)

  for basepath in list(subfolders):
    sf, f = scandir(basepath, exts)
    subfolders.extend(sf)
    filelist.extend(f)
  return subfolders, filelist
