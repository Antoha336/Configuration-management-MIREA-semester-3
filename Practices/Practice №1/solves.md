# Задания
* [Первоисточник](https://github.com/true-grue/kisscm/blob/main/pract/pract1.md)
* [Сохраненные локально](tasks.md)

# Решения
## Задача №1
```bash
cat /etc/passwd | sort
```
![image](https://github.com/user-attachments/assets/fb1947f4-4f33-4fff-a0af-9c4295425314)

## Задача №2
```bash
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```
![image](https://github.com/user-attachments/assets/ac840076-49d9-4f67-96b4-8d015cdb7e71)

## Задача №3
```bash
#!/bin/bash

message="$1"
length=${#message}

border="+-"
for (( i=0; i<length; i++ )); do
  border="${border}-"
done
border="${border}-+"

echo "$border"
echo "| $message |"
echo "$border"
```
![image](https://github.com/user-attachments/assets/03d9b3db-44bf-403c-bdc2-f45d61730665)

## Задача №4
```bash
#!/bin/bash

filename="$1"

grep -o -w '\b[_a-zA-Z][_a-zA-Z0-9]*\b' "$filename" | sort | uniq
```
![image](https://github.com/user-attachments/assets/69359fa2-d4a2-46bf-98bb-fd1afe1b201d)

## Задача №5
```bash
#!/bin/bash

filename="$1"

chmod +x $filename
mv $filename /usr/local/bin
```
![image](https://github.com/user-attachments/assets/ab1c4cd3-84f4-4524-a243-2c54af8c59bd)

## Задача №6
```bash
#!/bin/bash

filename="$1"
line=$(head -n 1 "$filename").c

if [[ $filename =~ \.(c)$ ]]; then
  if [[ $line =~ ^(\/\/) ]]; then
    echo "$filename has a comment"
  else
    echo "$filename doesn't have a comment"
  fi
elif [[ $filename =~ \.(js)$ ]]; then
  if [[ $line =~ ^(\/\*) ]]; then
    echo "$filename has a comment"
  else
    echo "$filename doesn't have a comment"
  fi
elif [[ $filename =~ \.(py)$ ]]; then
  if [[ $line =~ ^(\#) ]]; then
    echo "$filename has a comment"
  else
    echo "$filename doesn't have a comment"
  fi
else
  echo "$filename doesn't have a comment"
fi
```
![image](https://github.com/user-attachments/assets/0ec0fc71-35a7-43d6-823a-0d3a39f59027)

## Задача №7
```bash
#!/bin/bash

directory="$1"

hash=$(find "$directory" -type f -exec md5sum {} + | sort | uniq -w 32 -d | awk '{print $1}')
find "$directory" -type f -exec md5sum {} + | grep "$hash" | awk '{print $2}'
```
![image](https://github.com/user-attachments/assets/09682c9a-6a33-4d28-a9f4-c9a36806b57a)

## Задача №8
```bash
#!/bin/bash

directory=$1
ext=$2

mkdir -p ./temp
find "$directory" -type f -name "*.$ext" -exec cp {} ./temp +
tar -cf "${ext}_files.tar" ./temp
rm -R ./temp
```
![image](https://github.com/user-attachments/assets/3cee82d6-0e67-459a-a96d-4df8f8d9f96f)

## Задача №9
```bash
#!/bin/bash

input_file=$1
output_file=$2

touch $output_file
cat $input_file | sed "s/    /\t/g" > $output_file
```
![image](https://github.com/user-attachments/assets/d66d29e0-3efe-43b6-9db7-e9424cd67e21)

## Задача №10
```bash
#!/bin/bash

directory=$1

find $directory -size 0
```
![image](https://github.com/user-attachments/assets/2d3c227d-6154-4278-a733-45f34a899eb8)
