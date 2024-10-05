# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract3.md)
* [Сохраненные локально](https://github.com/Antoha336/Configuration-management-MIREA-semester-3/blob/main/Practices/Practice%20%E2%84%963/tasks.md)

# Решения
## Задача №1
```json
local create_student(name, group, age) = {
  age: age,
  group: group,
  name: name,
};

{
  groups: ["ИКБО-%d-20" % i for i in std.range(1, 24)],
  "students": [
    create_student("Иванов И.И.", "ИКБО-4-20", 19),
    create_student("Петров П.П.", "ИКБО-5-20", 18),
    create_student("Сидоров С.С.", "ИКБО-5-20", 18),
    create_student("Маркаданов А.А.", "ИКБО-10-23", 19),
  ],
  "subject": "Конфигурационное управление"
}
```

## Задача №3
Язык нулей и единиц.
```python
BNF = '''
E = 0 | 1 E | 1
'''
```

## Задача №4
Язык правильно расставленных скобок двух видов.
```python
BNF = '''
E = () | {} | ( E ) | { E } | E E
'''
```

## Задача №5
Язык выражений алгебры логики.
```python
BNF = '''
E = E & E | E OR E | ~ E | ( E ) | x | y
'''
```