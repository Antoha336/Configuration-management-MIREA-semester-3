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