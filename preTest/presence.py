#!/usr/bin/env python
###############################################################################
### presence.py
### Time-stamp: <Fri 2018-11-30 00:10 svarrette>
###
### Copyright (c) 2018 A. A.Z.A Ibrahim, S. Varrette
### .
###
###############################################################################

"""PRESENCE: Monitoring and Modelling the Performance Metrics of Mobile Cloud SaaS Web Services"""
import click
import pkg_resources
import os
import fcntl
import errno
import sys


from .cli.conf import conf


@click.group(invoke_without_command=True)
#CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
#@click.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('-v','--version', flag_value=True,help='Return the version of this script.')
def presence(ctx,version):
	"""
	These scripts are written to operatre the PRESENCE Framework.
		
	Select the sub-command to execute.
	"""
	if ctx.invoked_subcommand is None:
		if version:
			click.echo("This is PRESENCE version " + pkg_resources.require("presence")[0].version)
        else:
        	click.echo(ctx.get_help())


presence.add_command(conf)