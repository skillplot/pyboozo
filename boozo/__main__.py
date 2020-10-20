## Copyright (c) 2020 mangalbhaskar.
"""Create the required project structure and the environment configurations."""
__author__ = 'mangalbhaskar'


import os

import click

clear = lambda: os.system('clear')
clear()


from . import cli

@click.group()
def cmd():
  pass


cmd.add_command(cli.init)
cmd.add_command(cli.welcome)


if __name__ == "__main__":
  cmd()
