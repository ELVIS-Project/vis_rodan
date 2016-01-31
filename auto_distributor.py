import yaml
import os

author = 'Marina Borsodi-Benson'

with open('resource_types.yaml', 'r') as yamlFile:
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
	distributor += 'distributor.py'
	className += "Distributor"
	name += 'Distributor'
	mimetype = line['mimetype']

	if os.path.exists('tests/' + distributor):
		pass
	else:
		with open('distributor.txt', 'r') as distr:
			dstext = distr.read()
		dstext = dstext.replace('<<<distributor>>>', distributor)
		dstext = dstext.replace('<<<name>>>', name)
		dstext = dstext.replace('<<<classname>>>', className)
		dstext = dstext.replace('<<<author>>>', author)
		dstext = dstext.replace('<<<input>>>', inputPort)
		dstext = dstext.replace('<<<mimetype>>>', mimetype)
		target = open('test/' + distributor, 'w')
		target.write(dstext)
		target.close()