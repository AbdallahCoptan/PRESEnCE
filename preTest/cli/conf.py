#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: Configure Presence.
#######################################################################################################################

import click
import os

@click.command(short_help="Prints Resif's version information.")
@click.option('-o','--oper', default=1000,
				help='The number of operations per second.')
@click.option('-r','--rec', default=1000,
				help='The number of records per second.')
@click.option('-td','--thrd', default=1,
				help='The number of threads.')

def conf(ctx,oper,rec,thrd):
 	click.echo('All Presence default Values:')
 	click.echo('operations %s !' % oper)
 	click.echo('records %s !' % rec)
 	click.echo('threads %s !' % thrd)
 	return