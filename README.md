# ner_recognition

## скрипт на языке Python 3 
Скрипт запускается из консоли(файл Text_Processing.py)

параметры --input или -i - путь к папке с исходными текстами(абсолютный или относительный), значение по умолчанию ./texts/

параметры --output или -o - путь к папке с результатами(абсолютный или относительный), значение по умолчанию ./results/(в случае отсутствия папки она создается)

## Примеры запуска
Используем папки по умолчанию

python3 Text_Processing.py

Используем свои папки

python3 Text_Processing.py -i /home/user/ner_rules/ner_recognition/test_set -o ./ner_results 

В случае если в пути присутствует пробел необходимо взять путь в одинарные или двойные кавычки


## Формат выдачи
Записанные через пробел:

тип сущности, индекс символа с которого начинается сущность, длина в символах, сущность 

## Пример
ORG 161 3 CNN

LOC 221 6 Турции

PER 269 5 Путин

LOC 338 8 Стамбула
