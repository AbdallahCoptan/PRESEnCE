#!/usr/bin/env python
###############################################################################
### presence.py
### Time-stamp: <Fri 2018-11-30 00:10 svarrette>
###
### Copyright (c) 2018 A. A.Z.A Ibrahim, S. Varrette
### .
###
###############################################################################

"""PRESENCE: Monitoring and Modelling the Performance Metrics of Mobile Cloud SaaS Web Services
"""

import click
import pkg_resources
import os
import fcntl
import errno
import sys
import os

from .cli.config import config
from .cli.create import create
from .cli.run import run
from .cli.runUp import runUp
from .cli.check import check
from .cli.campaign import campaign

###############################################################################
# The presence group. Defines the name of the command. It is the "main" group.

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-v','--version', flag_value=True, help='Return the version of this script.')
def presence(ctx, version):
    """
    PRESENCE commandline interface.

    Select the sub-command to execute.
    """

    if ctx.invoked_subcommand is None:
        if version:
            click.echo("This is PRESENCE version " + pkg_resources.require("presence")[0].version)
        else:
            click.echo(ctx.get_help())

###############################################################################


presence.add_command(config)
presence.add_command(create)
presence.add_command(run)
presence.add_command(runUp)
presence.add_command(check)
presence.add_command(campaign)
