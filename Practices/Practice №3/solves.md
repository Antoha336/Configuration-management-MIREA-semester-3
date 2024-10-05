# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract3.md)
* [Сохраненные локально](https://github.com/Antoha336/Configuration-management-MIREA-semester-3/blob/main/Practices/Practice%20%E2%84%963/tasks.md)

# Решения
## Задача №1
```json
{
  groups: ["ИКБО-%d-20" % i for i in std.range(1, 24)],
    "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    {
      "age": 19,
      "group": "ИКБО-10-23",
      "name": "Маркаданов А.А."
    }
  ],
  "subject": "Конфигурационное управление"
}
```