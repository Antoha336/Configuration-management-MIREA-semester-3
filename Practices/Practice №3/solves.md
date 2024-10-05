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

## Задача №2
```haskell
let Group = Text
let Student = { age : Natural, group : Group, name : Text }

let create_student : Natural -> Text -> Text -> Student =
	\(age : Natural) -> \(group : Text) -> \(name : Text) ->
  { age = age, group = group, name = name }

let create_group : Natural -> Group =
	\(num : Natural) ->
	"ИКБО-" ++ (Natural/show num) ++ "-20"

let groups : List Group = [ 
	create_group 1,
	create_group 2,
	create_group 3,
	create_group 4,
  create_group 5,
	create_group 6,
	create_group 7,
	create_group 8,
	create_group 9,
	create_group 10,
	create_group 11,
	create_group 12,
	create_group 13,
	create_group 14,
	create_group 15,
	create_group 16,
	create_group 17,
	create_group 18,
	create_group 19,
	create_group 20,
	create_group 21,
	create_group 22,
	create_group 23,
	create_group 24,
]

let students : List Student = [ 
	create_student 19 (create_group 4) "Иванов И.И.", 
	create_student 18 (create_group 4) "Петров П.П.",
	create_student 18 (create_group 5) "Сидоров С.С.",
	create_student 19 (create_group 10) "Маркаданов А.А."
]

let subject = "Конфигурационное управление"

in { groups = groups, students = students, subject = subject }
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