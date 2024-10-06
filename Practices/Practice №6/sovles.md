# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract6.md)
* [Сохраненные локально](tasks.md)

# Решения
## Задача №1
$\displaystyle\int_{x}^{\infin}{\frac{dt}{t(t^{2}-1\log{t}}}=\int_{x}^{\infin}{\frac{1}{t\log{t}}\Bigg(\sum_{m}{t^{-2m}}\Bigg)}dt=\sum_{m}\int_{x}^{\infin}{\frac{t^{-2m}}{t\log{t}}}dt \overset{(u=t^{-2m})}{=}-\sum_{m}li(x^{-2m)}~~~Маркаданов~Антон~Алексеевич$

## Задача №2
```plantuml
@startuml

actor "Маркаданов Антон Алексеевич" as student
database Piazza as piazza
actor "Преподаватель" as teacher

teacher -> piazza : Публикация задачи
activate piazza
piazza --> teacher : Задача опубликована
deactivate piazza
...
student -> piazza : Поиск задач
activate piazza
piazza --> student : Получение задачи
deactivate piazza
...
student -> piazza : Публикация решения
activate piazza
piazza --> student : Решение опубликовано
deactivate piazza
...
teacher -> piazza : Поиск решений
activate piazza
piazza --> teacher : Решение найдено
teacher -> piazza : Публикация оценки
piazza --> teacher : Оценка опубликована
deactivate piazza
...
student -> piazza : Проверка оценки
activate piazza
piazza --> student : Оценка получена
deactivate piazza

@enduml
```
![plantuml](https://github.com/user-attachments/assets/aebba34c-853b-47a6-9033-9ed95cfc3c88)