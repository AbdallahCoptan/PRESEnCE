import yaml
import sys
import ruamel.yaml

def read_yml(filepath):
	"""Loading a yamel file"""
	with open(filepath,"r") as ymlfile:
		data = yaml.load(ymlfile) or {}
	return data

def print_yml(filepath):
	""" printing the yamel file"""
	with open(filepath, 'r') as ymlfile:
		cfg = yaml.load(ymlfile)
		print yaml.dump(cfg, default_flow_style=False)
	#for section in cfg:
	#	print(section)
	#	print(cfg[section])

def print_asYml(section):
	print yaml.dump(section, default_flow_style=False)

def write_yml(filepath, data):
	"""Dumps a yamel file"""
	with open(filepath,"w") as ymlfile:
		yaml.dump(data, ymlfile, default_flow_style=False )

def secExist(dictinary, section):
	""" check the existance of the section in a dictionary """
	if type(dictinary) is not dict:
		print "This is not a dictinary !!"
		return None
	if section in dictinary.keys():
		return True
	else:
		return False


def set(filepath, section,attribute = None, value = None, data = None):
	""" 
	set(filepath, '#section') to add a comment section
	set(filepath, '#section','#attribute','value') to add a commented attributes with value 
	set(filepath, section,attribute) to add a new attribute
	set(filepath, section,attribute, value) to add/ update existing attribute value
	set(filepath, section,data = data) to add a full section data directly
	"""
	config = read_yml(filepath)
	if type(config) is not dict:
		config = {}
	if attribute == None and value == None:
		config[section] = data
	if attribute != None and value == None:
		if not secExist(config,section):
			config[section] = {}
		config[section][attribute] = {}
	if attribute != None and value != None:
		if not secExist(config,section):
			config[section] = {}
		config[section][attribute] = {}
		config[section][attribute] = value
	else:
		if config[section] == '' or config[section] == None or config[section][attribute] == None or config[section][attribute] == '':
			config[section] = {}
			config[section][attribute] = {}
		config[section][attribute] = value
	write_yml(filepath,config)


def get(filepath, section=None,attribute=None):
	config = read_yml(filepath)
	if not secExist(config,section): 
		print 'Section: There is no section with this name'
		sys.exit(50)
		value = None
	#if config[section][attribute] == None or config[section][attribute] == '':
	#	pass
	if attribute == None:
		value = config[section]
	else:
		value = config[section][attribute]
	return value


def delet(filepath,section,attribute = None,value = False, Allattributes = False):
	""" delete the entire section, or its attributes : delet(f,section) | delet(f, section, )
		delete the entire attribute: delet(f,section, attribute) 
		delet only the value :  delet(f, section, attribute, value = True)
	"""
	config = read_yml(filepath)
	if secExist(config,section):
		if attribute != None:
			del config[section][attribute]
		if attribute != None and value == True:
			config[section][attribute] = {}
		if Allattributes == True:
			config[section] = {}
		if attribute == None and Allattributes == False:
			del config[section]
		write_yml(filepath,config)
	else:
		print "error: This section is not exist to delete !!"
		sys.exit(50)

def add_comment(filepath, comment, start = True):
	comment = "##"+comment+"\n"
	d = read_yml(filepath)
	if start == True:
		with open(filepath, "w") as f:
			f.write(comment)
			ruamel.yaml.dump(d, f, Dumper=ruamel.yaml.RoundTripDumper,default_flow_style=False, width=50, indent=8)
	else:
		with open(filepath, "w") as f:
			f.write(yaml.dump(comment,default_flow_style = False))
			#ruamel.yaml.dump(f, d, Dumper=ruamel.yaml.RoundTripDumper,default_flow_style=False, width=50, indent=8)


def newY(filepath):
		#comment = "#this is a new empty yaml file"
		dataMap = dict( Section =  dict(Attribute = '<value>'))
		write_yml(filepath,dataMap)


def get_default_path():
	DoNotTouch = 'Config/DoNotTouch/default.txt'
	with open(DoNotTouch, 'r') as file:
		temp = file.readline()
	return temp