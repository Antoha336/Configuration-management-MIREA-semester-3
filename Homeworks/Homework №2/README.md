# Механизм работы
Скрипт парсит зависимости пакета платформы .NET из конфиг-файла, генерирует .dot файл с инструкциями для утилиты dot из GraphViz, а затем создает визуализацию зависимостей в виде картинки.
# Использование
## Содержимое конфиг-файла
```xml
<?xml version="1.0" encoding="utf-8" ?>
<Configuration>
    <GraphvizPath>путь до утилиты dot (или просто dot, если прописано в PATH)</GraphvizPath>
    <PackagePath>ссылка на пакет на сайте www.nuget.org</PackagePath>
</Configuration>
```
## Запуск
### В общем виде
```bash
python main.py <config_file_path>
```
### В случае репозитория
```bash
python main.py config.xml
```
# Требования
* Python 3.11
* Утилита dot из GraphViz
* Конфиг-файл с требуемым содержимым