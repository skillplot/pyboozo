## Copyright (c) 2020 mangalbhaskar.
"""Create the required project structure and the environment configurations."""
__author__ = 'mangalbhaskar'


import os
import pathlib
import shutil
import sys

import click

# this = sys.modules[__name__]
this_dir = os.path.dirname(__file__)


from .boot._log_ import log

from .boot import bootstrap
from .boot.env import EnvCfgo
from .utils import snek
from .utils import color


default_name = 'boozo'
default_prefix = 'BZO'
# default_root = os.path.dirname(os.getcwd())
default_root = pathlib.Path(this_dir).parent.parent.as_posix()


def echo(d):
  log.info("__main__: default_root: {}".format(d))
  pass


@click.command()
@click.option('--name',
              prompt=color.text('Application name', cc=color.on_cya),
              default=default_name,
              help='Name of the main application; max: 7 chars [a-z]')
@click.option('--root',
              prompt=color.text('Root directory for application', cc=color.on_cya),
              type=click.Path(exists=True),
              default=default_root,
              help='Absolute path for application Root directory. Defaults to current directory.')
@click.option('--prefix',
              prompt=color.text('Prefix for environment variables', cc=color.on_cya),
              default=default_prefix,
              help='Prefix ensures the unique namespace; max: 3 [a-z] chars')
@click.option('--timestamp',
              is_flag=True,
              default=True,
              #prompt=True,
              help='Easier to create multiple directories and switch between if used along with softlink')
@click.option('--mobile',
              is_flag=True,
              default=True,
              #prompt=True,
              help='Create MOBILE specific directories.')
@click.option('--data',
              is_flag=True,
              default=True,
              #prompt=True,
              help='Create DATA specific directories.')
@click.option('--vm',
              is_flag=True,
              default=True,
              #prompt=True,
              help='Create VIRTUALENV specific directories.')
@click.option('--gitkeep',
              is_flag=True,
              default=False,
              #prompt=True,
              help='Create the empty hidden file (.gitkeep) in each directory')
def init(**kwargs):
  """Create the directories, smylinks and the configuration files."""
  try:
    ## main home paths
    __envars = {}
    __envars['_NAME'] = kwargs['name']
    __envars['_PREFIX'] = kwargs['prefix']
    __envars['_ROOT'] = kwargs['root']
    __envars['_IS_MOBILE_DIR'] = kwargs['mobile']
    __envars['_IS_DATA_DIR'] = kwargs['data']
    __envars['_IS_VMHOME'] = kwargs['vm']

    echo(__envars['_ROOT'])

    envcfgo = EnvCfgo(__envars)

    _dirpaths = [envcfgo._CONFIG_ROOT]+ \
      envcfgo._DIR_PATH+envcfgo._DATA_DIR_PATH+envcfgo._MOBILE_DIR_PATH+ \
      [envcfgo._VMHOME, envcfgo._PYVENV_PATH]

    color.cprint("Creating setup...")
    bootstrap.make_dirs(*_dirpaths, gitkeep=kwargs['gitkeep'])

    gitignore_filepath = os.path.join(envcfgo._HOME,'.gitignore')
    gitignore_filepath_src = os.path.join(this_dir,'data','gitignore')
    if not os.path.isfile(gitignore_filepath) and os.path.isfile(gitignore_filepath_src):
      ## copy pre-configured gitignore template, if it does not exists to prevent overriding customized file
      shutil.copy(gitignore_filepath_src, gitignore_filepath)

    if kwargs['timestamp']:
      bootstrap.make_links(*envcfgo._DATA_DIR_PATH)

    bootstrap.make_links(**envcfgo._LINK)

    kwargs = envcfgo.get_kwargs()
    log.debug("kwargs: {}".format(kwargs))

    bootstrap.generate_cfgyml(**kwargs)
    env_filepath = bootstrap.generate_envsh(**kwargs)
    bootstrap.generate_aliassh(**kwargs)
    bootstrap.generate_exportsh(**kwargs)

    color.cprint("Hurrayy!!! Project [{}] structure Initialized!".format(__envars['_NAME']), cc=color.bired)
    color.cprint("Shape the Future - Code, Eat, Sleep & Repeat.\n", cc=color.biyel)
    color.cprint("Project Root: ", cc=color.bpur, es=__envars['_ROOT'])
    color.cprint("Main application directory: ", cc=color.bpur, es=os.path.join(__envars['_ROOT'], __envars['_NAME']))

    color.cprint(snek.fancy)
    color.cprint("Paste it in file: ", cc=color.biyel, es="~/.bashrc")
    color.cprint("source {}\n".format(env_filepath), cc=color.bblu)
  except:
    import traceback
    traceback.print_exception(*sys.exc_info()) 


@click.command()
def welcome():
  click.echo('Welcome')
