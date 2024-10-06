import json

with open('civgraph.json', 'r') as file:
    packages = json.loads(file.read())

makefile = open('Makefile', 'w')

makefile.write('.PHONY = clean\n\n')

for key in packages:
    dependencies = packages[key]
    makefile.write(f'{key}: {key}.done\n\n')
    makefile.write(f'{key}.done: {" ".join([f"{package}.done" for package in dependencies])}\n')
    makefile.write(f'\t@echo {key}\n')
    makefile.write(f'\t@type nul > {key}.done\n\n')

makefile.write('clean:\n')
makefile.write('\t@del /F *.done\n')

makefile.close()