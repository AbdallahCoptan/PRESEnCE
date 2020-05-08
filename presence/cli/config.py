#######################################################################################################################
# Author: Abdallah Ibrahim
# Mail: abdallah.ibrahim@uni.lu
# Overview: Configure Presence.
#######################################################################################################################

import click
import os
from yml import *
from Table import Table


def get_default_path():
	DoNotTouch = 'Config/DoNotTouch/default.yml'
	return get(DoNotTouch, 'configdir', 'dir')
def set_default_path(directory):
	DoNotTouch = 'Config/DoNotTouch/default.yml'
	set(DoNotTouch, 'configdir', 'dir', directory)


@click.command(short_help="Prints Presence's config information.")
#servers
#@click.option('-R','--redis', flag_value=True, help='Redis Server.')
#@click.option('-Mem','--memcached', flag_value=True, help='Memcached Server.')
#@click.option('-Mdb','--mongodb', flag_value=True, help='Mongodb Server.')
#@click.option('-A','--apache', flag_value=True, help='Apache Server.')
#@click.option('-PSQL','--postegresql', flag_value=True, help='PostegreSQL Server.')
#@click.option('-IpS','--iperfserver', flag_value=True, help='Iperf Server.')
#options
@click.option('-l','--load','load', flag_value=True, help='Load a new or the existing configuration file.')
@click.option('-W','--where', flag_value=True, help='Return the dirctory or the file path of the configuration file.')
@click.option('-dir','--configdir', 'configdir',default= 'Config/config.yml' ,help='Defines an alternative path to load the configuration from. \n default = (Config/config.yml)')
@click.option('-p','--print', flag_value=True, help='Print the whole configuration file.')
@click.option('--asTxt','asTxt', flag_value=True, help='Print the whole configuration file as text dictionary.')
@click.option('--asYml','asYml', flag_value=True, help='Print the whole configuration file as yaml dictionary, as looks like in the configuration file.')
@click.option('-s','--set', flag_value=True, help='Set the configuration of a specific server.')
@click.option('-g','--get', flag_value=True, help='Get the configuration of a specific server.')
@click.option('-d','--delete', flag_value=True, help='Delete the configuration of a specific server.')


@click.option('-k','--key', default='<key>', help='The attribute name to be add in the section if needed \n default value is key = <key>')
@click.option('-v','--value', default='<value>', help='The value of the attribute in a specific section if needed \n default value is value = <value>')
@click.option('-sec','--section', default='<section>', help='The section name to be added in the config file if needed \n default value is section = <section>')
@click.option('-dic','--dictionary', default=dict(), help='The dictionary to be added in the config file if needed \n default value is dictionary = dict()')


def config(**kwargs):
	""" 
	PRESENCE config commandline interface.

    Select the [options: set | get | print | load | delete] 

    with [options: section | key | value] to update/set the configurations 


	"""
	#load the existing or a new configurations
	if kwargs['load']:
		click.echo('--------------------------------------------------------------------------')
		set_default_path(kwargs['configdir'])
		directory = get_default_path()
		click.echo('The configuration file is loaded in the directory:  %s' % directory)
		click.echo('--------------------------------------------------------------------------')
	
	#where the configuration are saved
	elif kwargs['where']:
		click.echo('--------------------------------------------------------------------------')
		directory = get_default_path()
		click.echo('The configuration file is in the directory:  %s' % directory)
		click.echo('--------------------------------------------------------------------------')

	#printing the configurations
	elif kwargs['print']:
		if kwargs['asTxt']:
			click.echo('--------------------------------------------------------------------------')
			click.echo('Presence configurations: \n')
			configfile = read_yml(get_default_path())
			click.echo(configfile)
			click.echo('--------------------------------------------------------------------------')
		elif kwargs['asYml']:
			click.echo('------------------------------------')
			click.echo('Presence configurations: \n')
			configfile = print_yml(get_default_path())
			click.echo(configfile)
			click.echo('------------------------------------')
		else:
			click.echo('--------------------------------------------------------------------------')
			click.echo('Please indicate, would you like to print asTxt | asYml .')
			click.echo('--------------------------------------------------------------------------')
			exit(50)

	# get a section or attribute values
	elif kwargs['get']:
		directory = get_default_path()
		if kwargs['section'] != '<section>' and kwargs['key'] == '<key>':
			section = get(directory, kwargs['section'])
			if kwargs['asYml']:
				#click.echo(yaml.dump(section, default_flow_style=False))
				print_asYml(section)
			else:
				click.echo(section)
		elif kwargs['section'] != '<section>' and kwargs['key'] != '<key>':
			value = get(directory, kwargs['section'], kwargs['key'])
			if kwargs['asYml']:
				#click.echo(yaml.dump(value, default_flow_style=False))
				print_asYml(value)
			else:
				click.echo(value)
		elif kwargs['key'] != '<key>' and kwargs['section'] == '<section>':
			click.echo('Invalid compination, you need to indicate from which section to get the attribute : (%s)' % kwargs['key'])
			exit(50)
		else: 
			click.echo('Invalid compination, you need to indicate either section or section with key to get the attribute !! ')
			exit(50)
	#set a section, attribute or a value
	elif kwargs['set']:
		directory = get_default_path()
		if kwargs['section'] == '<section>' and kwargs['key'] == '<key>' and kwargs['value'] == '<value>':
			click.echo('Good compination, but you need to indicate the new names either for section, attribute or value to be added !! ')
			click.echo('The default values will be added to the configuration file liek: <section> : <key> : <value>')
			set(directory, kwargs['section'], kwargs['key'], kwargs['value'])
		elif kwargs['section'] != '<section>' and  kwargs['dictionary'] != dict():
			set(directory, kwargs['section'], data = kwargs['dictionary'])
		else:
			set(directory, kwargs['section'], kwargs['key'], kwargs['value'])
			click.echo('The new values have been added !!')
	# delete a section, or attribute
	elif kwargs['delete']:
		directory = get_default_path()
		if kwargs['section'] != '<section>' and kwargs['key'] == '<key>' and kwargs['value'] == '<value>':
			char = click.prompt('would you like to delet only the all attributes of this section [Y/n]?', type=str, default = 'n')
			if char == 'n':
				delet(directory, kwargs['section'])
			if char == 'Y' or char == 'y':
				delet(directory, kwargs['section'], Allattributes = True)
		elif kwargs['section'] != '<section>' and kwargs['key'] != '<key>':
			char = click.prompt('would you like to delet only the value of this attribute [Y/n]?', type=str, default = 'n')
			if char == 'n':
				delet(directory, kwargs['section'], kwargs['key'])
			if char == 'Y' or char == 'y':
				delet(directory, kwargs['section'], kwargs['key'], value = True)
		else:
			click.echo('Please indicate name for [section]| [section & attribute]')
			click.echo('otherwise, the section with the default section value will be dellected at all.')
			delet(directory, kwargs['section'])

	else:
		click.echo('Attention...\n')
 		click.echo('You need to decide on set | get | print | load | delete what from the Presence configurations\n')
 		click.echo('Usage: presence config [set | get | print | load | delete] \n')
		t = Table(titles=['Options','Usage'])
 		t.add_row(['load','presence config --load [-dir [new]]'])
 		t.add_row(['print','presence config  --print [--asTxt | --asYml]'])
 		t.add_row(['where','presence config  --where'])
 		t.add_row(['set','presence config --set [server and [attribute | value] | [data dictionary]'])
 		t.add_row(['get','presence config  --get [server & attribute] | [server]'])
 		t.add_row(['delete','presence config --delete [section and  attribute] | [section and Allattributes] | [section and attribute and value]'])
 		click.echo('check the following table which summerize PRESENCE\'s config options:\n\n %s' % t)

 		click.echo('\n try the --help command:  presence config --help   \n')


	return