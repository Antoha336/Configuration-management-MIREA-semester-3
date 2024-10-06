import json

with open('civgraph.json', 'r') as file:
    packages = json.loads(file.read())

makefile = open('Makefile', 'w')

for key in packages:
    dependencies = packages[key]
    makefile.write(f'{key}: {" ".join(dependencies)}\n')
    makefile.write(f'\t@echo {key}\n\n')

makefile.close()