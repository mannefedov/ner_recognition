# -*- coding: utf-8 -*-
import codecs
import os
import json
import re


def open_file(filename):
    """
    Функция возвращает файл, прочитанный в кодировке utf-8
    :param filename: имя файла с расширением
    :return: строка, содержащая полный исходный текст
    """
    fh = codecs.open(filename + '.txt', 'r', encoding='utf-8')
    fh = fh.read()
    fh = fh.replace("^", " ")
    fh = fh.replace("\\", " ")
    fh = fh.replace("&", " ")
    fh += '\n.'
    return fh

# ----------- УКАЗАТЬ В ПЕРЕМЕННОЙ path ПУТЬ К СЛОВАРЯМ -----------
def open_dictionary(filename):
    """
    Функция возвращает импортированный словарь, прочитанный в кодировке utf-8
    :param filename: имя файла с расширением
    :return: список строк словаря
    """
    cwd = os.getcwd()

    path = "/Users/ulyanasidorova/Documents/NER_repository/dictionaries"
    os.chdir(path)
    fh = codecs.open(filename + ".txt", 'r', encoding='utf-8')
    imported_dictionary = []
    for line in fh:
        line = line.strip()
        imported_dictionary.append(line)
    imported_dictionary.sort()
    os.chdir(cwd)
    return imported_dictionary


def write_in_file(text, filename, separator=' ', path="/Users/ulyanasidorova/Downloads/XXX/raw"):
    f = open(filename + '.txt', 'w', encoding='utf-8')
    cwd = os.getcwd()
    os.chdir(path)
    for token in text:
        array = []
        for key in token:
            array.append(str(token[key]))
        f.write(separator.join(array))
        f.write('\n')
    f.close()
    os.chdir(cwd)
    # print('-----------------------------------')
    # print('Content is in file: ' + filename + '.txt.')
    # print('-----------------------------------')


# def write_as_json(text, filename, path='/Users/ulyanasidorova/Documents/UPD — копия 2'):
#     pwd = os.getcwd()
#     os.chdir(path)
#     f = open('j_' + filename + ".json", 'w', encoding='utf-8')
#     text = json.dumps(text)
#     f.write(text)
#     # print("===================")
#     # print("Content is in file: " + filename + ".json.")
#     # print("===================")
#     os.chdir(pwd)
#     return True


def write_as_object(text, filename, path):
    pwd = os.getcwd()
    os.chdir(path)
    f = open(filename + ".txt", 'w', encoding='utf-8')
    for line in text:
        f.write(line + '\n')
    print("===================")
    print("Извлеченные сущности находятся в файле: " + filename + ".txt.")
    print("Файл находится в папке: " + path + ".")
    print("===================")
    os.chdir(pwd)
    return True


def open_json(filename, path):
    pwd = os.getcwd()
    os.chdir(path)
    with open('j_' + filename + '.json', 'r') as f:
        text = json.load(f)
    os.chdir(pwd)
    return text

#
# def write_in_file_result(result, filename,separator=' '):
#     f = open(filename + '.txt', 'w', encoding = 'utf-8')
#     array = []
#     for line in result:
#         x = []
#         if 'PERSON' in line or 'ORG_I' in line or 'ORG_B' in line or 'LOC' in line:
#             x.append(line[1], str(line[0]), str(line[2]))
#             array.append(x)
#     for item in array:
#         f.write(separator.join(array))
#         f.write('\n')
#     f.close()
#     # print ('-----------------------------------')
#     # print('Content is in file: ' + filename + '.txt.')
#     # print ('-----------------------------------')
#
#
# def write_in_file_result(result, filename,separator=' '):
#     f = open(filename + '.objects.txt', 'w', encoding = 'utf-8')
#     x = []
#     for line in result:
#         if 'PERSON' or 'ORG_I' in line or 'ORG_B' in line or 'LOC' in line:
#             x.append(line)
#         for item in x:
#             item = str(item)
#             f.write(separator.join(item))
#             f.write('\n')
#     f.close()
#     # print ('-----------------------------------')
#     # print('Content is in file: ' + filename + '.objects.txt.')
#     # print ('-----------------------------------')