# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract4.md)
* [Сохраненные локально](tasks.md)

# Решения
## Тестирование make
Был создан Makefile и вызвана команда make.
![image](https://github.com/user-attachments/assets/234f7536-594e-4f5d-a38f-45052444e2ce)
## Визуализация файоа civgraph.txt
![image](https://github.com/user-attachments/assets/4a479121-8b78-445d-8438-c940d50a5d32)
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

## Задача №3
```python
import json

with open('civgraph.json', 'r') as file:
    packages = json.loads(file.read())

makefile = open('Makefile', 'w')

makefile.write('.PHONY: clean\n\n')

for key in packages:
    dependencies = packages[key]
    makefile.write(f'{key}: {key}.done\n\n')
    makefile.write(f'{key}.done: {" ".join([f"{package}.done" for package in dependencies])}\n')
    makefile.write(f'\t@echo {key}\n')
    makefile.write(f'\t@type nul > {key}.done\n\n')

makefile.write('clean:\n')
makefile.write('\t@del /F *.done\n')

makefile.close()
```
![image](https://github.com/user-attachments/assets/63b4974a-6456-4c4c-b36d-acad79762254)

## Задача №4
```makefile
.PHONY = all clean archive compile

prog.exe: prog.c data.c
	gcc prog.c data.c -o prog

compile: prog.exe

files.lst:
	dir /B > files.lst

distr.zip: compile files.lst
	7z a distr.zip *.*

archive: distr.zip

clean:
	del /F prog.exe files.lst distr.zip

all: compile archive clean
```
### Запуск без запуска других задач
![image](https://github.com/user-attachments/assets/d381311f-d684-4bb4-a50e-4940f3d7bfc8)
### Запуск с запуском других задач
![image](https://github.com/user-attachments/assets/b4273e37-e179-4d07-8138-a2d709afe0ac)
На выполнении задачи all видно, что при запуске других задач уже выполненные работы не исполняются.