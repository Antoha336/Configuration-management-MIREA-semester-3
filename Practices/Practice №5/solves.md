# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract5.md)
* [Сохраненные локально](tasks.md)

# Решения
## Задача №1
![image](https://github.com/user-attachments/assets/42619f98-5206-463f-817a-66407464cd91)

## Задача №2
```shell
>git init
Initialized empty Git repository in D:/Projects/git test/.git/
>git config user.name coder1
>git config user.email coder1@kisscm.com
>git add prog.py
>git commit -m "initial commit"
[main (root-commit) fbab2f1] initial commit
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py
```

## Задача №3
### Команды
```shell
git init --bare server.git
cd "git test"
git remote add server ../server.git
git remote -v
git push server main
git clone ../server.git "git test 2"
cd "git test 2"
git config user.name coder2
git config user.email coder2@kisscm.com
git add readme.md
git commit -m "добавление readme-файла"
cd ..
echo "Автор: coder1" >> readme.md
git add readme.md
git commit -m "добавление информации об авторстве"
git push server main
cd "git test 2"
git pull origin main
echo ", coder2\n" >> readme.md
git add readme.md
git commit -m "добавление информации об авторстве"
git push origin main
git log
```
### Содержимое логов
```shell
commit 7f495b949cace0b31f5f0c2294be7f7050faefb8 (HEAD -> main, origin/main, origin/HEAD)
Author: coder2 <coder2@kisscm.com>
Date:   Sun Oct 6 15:15:25 2024 +0300

    добавление информации об авторстве

commit d689a8278ec434eff36489c3cb2021406cfc83bb
Author: coder1 <coder1@kisscm.com>
Date:   Sun Oct 6 15:12:59 2024 +0300

    добавление информации об авторстве

commit 370c605de197bdfab02804fda6a1183e9ccd710e
Author: coder2 <coder2@kisscm.com>
Date:   Sun Oct 6 15:11:31 2024 +0300

    добавление readme-файла

commit fbab2f1aba868536893c175d838123a6f1f928d4
Author: coder1 <coder1@kisscm.com>
Date:   Sun Oct 6 14:54:04 2024 +0300

    initial commit
```

## Задача №4
### Код
```python
import subprocess

try:
    result = subprocess.run(
        args=['git', 'rev-list', '--all'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    result.check_returncode()

    result = result.stdout.splitlines()
except subprocess.CalledProcessError as e:
    result = []

for obj in result:
    try:
        result = subprocess.run(
            args=['git', 'cat-file', '-p', obj], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        result.check_returncode()
        
        print(f"Содержимое {obj}:\n{result.stdout}\n{'-'*60}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения содержимого {obj}")
```
### Пример вывода
```text
------------------------------------------------------------
Содержимое 537b2db921f29d104343671932b353c2369aca41:
tree ac246d3eea477356e0dca5633c530a23eb7dc21a
parent 9dbe513a2b206da6ffa18fd91541874c1648ed93
author Antes <coderasylum@gmail.com> 1726951163 +0300
committer Antes <coderasylum@gmail.com> 1726951163 +0300

refactor(hw в„–1): change the way of storing file in system

------------------------------------------------------------
Содержимое 9dbe513a2b206da6ffa18fd91541874c1648ed93:
tree 399940ff2e9652f8f5bf842fda2c39d4ae4c6f62
parent d6ddba11a81eaf015f203b054c3411dbf240707f
author Antes <coderasylum@gmail.com> 1726948856 +0300
committer Antes <coderasylum@gmail.com> 1726948856 +0300

refactor(hw в„–1): separate logic of interpritating pathes

------------------------------------------------------------
Содержимое d6ddba11a81eaf015f203b054c3411dbf240707f:
tree bcea8881ace9c5b431a0efa9448406cc37915781
parent dcae76f247b9b1afadb122bf1c651df7ab12cdd0
author Antes <coderasylum@gmail.com> 1726946185 +0300
committer Antes <coderasylum@gmail.com> 1726946185 +0300

feat(hw в„–1): add cd command
------------------------------------------------------------
```