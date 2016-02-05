import yaml
import os
import shutil

author = 'Marina Borsodi-Benson'

if os.path.exists('../wrappers/resource_distributors'):
	shutil.rmtree('../wrappers/resource_distributors')
	
os.makedirs('../wrappers/resource_distributors')

init = open('../wrappers/resource_distributors/__init__.py', 'w')
init.write('from rodan.jobs import module_loader\n')

with open('../resource_types.yaml', 'r') as yamlFile:
	contents = yaml.load(yamlFile)

for line in contents:

	desc = line['description'].split()
	distributor = ''
	className = 'VR'
	name = ''
	
	x=0
	while x < len(desc) and desc[x] != 'Indexer':
		distributor += desc[x].lower() + '_'
		className += desc[x]
		x += 1

	x=0
	while x < len(desc) and desc[x][0] != '(':
		name += desc[x] + ' '
		x += 1

	inputPort = name
	distributor += 'distributor'

	init.write("\nmodule_loader('rodan.jobs.vis-rodan.wrappers.resource_distributors." + distributor + "')")

	distributor += '.py'

	className += 'Distributor'
	name += 'Distributor'
	mimetype = line['mimetype']

	with open('distributor_template.txt', 'r') as distr:
		dstext = distr.read()
	dstext = dstext.replace('<<<distributor>>>', distributor)
	dstext = dstext.replace('<<<name>>>', name)
	dstext = dstext.replace('<<<classname>>>', className)
	dstext = dstext.replace('<<<author>>>', author)
	dstext = dstext.replace('<<<input>>>', inputPort)
	dstext = dstext.replace('<<<mimetype>>>', mimetype)

	target = open('../wrappers/resource_distributors/' + distributor, 'w')
	target.write(dstext)
	target.close()