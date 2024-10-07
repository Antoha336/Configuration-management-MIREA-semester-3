# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract2.md)
* [Сохраненные локально](tasks.md)

# Решения
## Задача №1
### Для просмотра служебной информации
```shell
pip show matplotlib
```
![image](https://github.com/user-attachments/assets/f71cab9c-78e2-4097-bbd9-3d0717c63012)
* Name - название
* Version - версия
* Summary - краткое описание
* Home-page - ссылка на сайт
* Author - авторы
* Author-email - электронные почты создателей
* Location - метоснахождение установленное
* Requires - список зависимостей
* Required-by - список пакетов, для которых данный пакет выступает зависимостью
### Для получения пакета без менеджера пакетов, прямо из репозитория
```shell
git clone https://github.com/matplotlib/matplotlib.git
cd matplotlib
python setup.py install
```

## Задача №2
### Для просмотра служебной информации
```shell
npm view express
```
![image](https://github.com/user-attachments/assets/29a1f3ec-5e76-4510-a1bf-bb95fa397491)
* название и версия
* описание
* сайт
* keywords - ключевые слова
* dist - информация по дистрибутиву
* dependencies - список зависимостей
* maintainers - список создателей
### Для получения пакета без менеджера пакетов, прямо из репозитория
```shell
git clone https://github.com/expressjs/express.git
var moduleName = require("path/to/express.js") # Добавить в файл проекта
```

## Задача №3
```python
from graphviz import Digraph

# Для matplotlib
matplotlib_graph = Digraph(comment='Matplotlib Dependencies')
matplotlib_graph.attr(rankdir='LR')
matplotlib_graph.node('matplotlib', 'matplotlib', shape='box')

dependencies_matplotlib = [
    'numpy', 'cycler', 'kiwisolver', 'packaging', 'pyparsing', 'pillow', 'contourpy', 'fonttools'
]
for dep in dependencies_matplotlib:
    matplotlib_graph.node(dep, dep, shape='ellipse')
    matplotlib_graph.edge('matplotlib', dep)

# Для express
express_graph = Digraph(comment='Express Dependencies')
express_graph.attr(rankdir='LR')
express_graph.node('express', 'express', shape='box')

dependencies_express = [
    'accepts', 'body-parser', 'cookie', 'debug', 'finalhandler', 'array-flatten', 
    'content-disposition', 'http-errors', 'qs', 'etag', 'merge-descriptors', 'safe-buffer'
]
for dep in dependencies_express:
    express_graph.node(dep, dep, shape='ellipse')
    express_graph.edge('express', dep)

matplotlib_graph.render('matplotlib_dependencies', format='png')
express_graph.render('express_dependencies', format='png')
```
![express_dependencies](https://github.com/user-attachments/assets/993d615c-75a1-41ed-9938-e4af308a12b9)
![matplotlib_dependencies](https://github.com/user-attachments/assets/abd72afa-be99-4cd2-b5cc-0c1333d25845)

## Задача №4
### Код для MiniZinc
```minizinc
include "globals.mzn";

var 0..9: digit_1;
var 0..9: digit_2;
var 0..9: digit_3;
var 0..9: digit_4;
var 0..9: digit_5;
var 0..9: digit_6;

constraint digit_1 + digit_2 + digit_3 = digit_4 + digit_5 + digit_6;
constraint all_different([digit_1, digit_2, digit_3, digit_4, digit_5, digit_6]);

solve minimize digit_1 + digit_2 + digit_3;

output [show(digit_1),show(digit_2),show(digit_3),show(digit_4),show(digit_5),show(digit_6)];
```
### Результата
![image](https://github.com/user-attachments/assets/07faafae-45fd-4d91-9016-8212ae6c0934)

### Ответ: 620431

## Задача №5
### Код для MiniZinc
```minizinc
array [1..2] of var 0..1: icons;
array [1..6] of var 0..1: menu;
array [1..5] of var 0..1: dropdown;

var 1..2: icons_version;
var 1..6: menu_version;
var 1..5: dropdown_version;

% Условие установки пакетов в единичном или нулевом экземплярах
constraint sum(icons) <= 1;
% Это также определение тревобания root (должна быть установлена любая версия menu)
constraint sum(menu) <= 1;
constraint sum(dropdown) <= 1;

% Установка условий от root
% Установка первой версии icons для root => вторую версию установить нельзя (т.к. должна быть установлена только одна или ноль)
constraint icons[2] == 0;

% Установка условий производных пакетов
% В случае первой версии menu подходит первая версия dropdown
constraint menu[1] = dropdown[1];
% В случае второй и выше версии menu подходит любая версия dropdown выше первой
constraint forall (i in 2..6) (menu[i] <= dropdown[5] + dropdown[2]);
% В случае второй и выше версии dropdown подходил любая версия icons выше первой
constraint forall (i in 2..5) (dropdown[i] <= icons[2]);

% Для каждого массива пробегаем и находим установленную версию
constraint forall(i in 1..2) (
  if icons[i] == 1
  then icons_version=i
  else true
  endif
);

constraint forall(i in 1..6) (
  if menu[i] == 1
  then menu_version=i
  else true
  endif
);

constraint forall(i in 1..5) (
  if dropdown[i] == 1
  then dropdown_version=i
  else true
  endif
);

output [
"icons version: ", show(icons_version), "\n",
"menu version: ", show(menu_version), "\n",
"dropdown version: ", show(dropdown_version)
];
```
### Результат
![image](https://github.com/user-attachments/assets/40035a4f-839e-4467-a059-e7d57d6e566b)

Цифры это индексы (начиная с 1) в таблицах версий на картинке:

![image](https://github.com/user-attachments/assets/922e221b-ba11-4f66-95ed-c8f4278981cb)
### Ответ
* menu: 1.0.0
* icons: 1.0.0
* dropdown: 1.8.0
