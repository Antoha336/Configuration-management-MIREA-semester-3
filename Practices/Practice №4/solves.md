# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract4.md)
* [Сохраненные локально](https://github.com/Antoha336/Configuration-management-MIREA-semester-3/blob/main/Practices/Practice%20%E2%84%964/tasks.md)

# Решения
Был создан Makefile и вызвана команда make.

![image](https://github.com/user-attachments/assets/234f7536-594e-4f5d-a38f-45052444e2ce)

## Задача №1
```python
import json

with open('civgraph.json', 'r') as file:
    packages = json.loads(file.read())

makefile = open('Makefile', 'w')

for key in packages:
    dependencies = packages[key]
    makefile.write(f'{key}: {" ".join(dependencies)}\n')
    makefile.write(f'\t@echo {key}\n\n')

makefile.close()
```
![image](https://github.com/user-attachments/assets/f3a21c18-1413-4811-957e-ca4d74e6a1e0)

## Задача №2
```python
import json

with open('civgraph.json', 'r') as file:
    packages = json.loads(file.read())

makefile = open('Makefile', 'w')

for key in packages:
    dependencies = packages[key]
    makefile.write(f'{key}: {key}.done\n\n')
    makefile.write(f'{key}.done: {" ".join([f"{package}.done" for package in dependencies])}\n')
    makefile.write(f'\t@echo {key}\n')
    makefile.write(f'\t@type nul > {key}.done\n\n')

makefile.close()
```
![image](https://github.com/user-attachments/assets/c39d84e4-7c38-42d4-8976-bfa7af1e4899)
![image](https://github.com/user-attachments/assets/64f12675-3a16-4706-bd50-becbcc3c20d9)
