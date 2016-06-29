# -*- coding: utf-8 -*-
import pprint
import Useful_functions as Use
import Ngrams as Ng
import json
from pymystem3 import Mystem
m = Mystem()



dict_descriptors_LOC = Use.open_dictionary("dict_descriptors_LOC")
dict_descriptors_ORG = Use.open_dictionary("dict_descriptors_ORG")
dict_descriptors_ORG_PER = Use.open_dictionary("dict_descriptors_ORG_PER")
dict_PER_NAMES_popular = Use.open_dictionary("dict_PER_NAMES_popular")
dict_LOC = Use.open_dictionary("dict_LOC")
dict_LocOrg = Use.open_dictionary("dict_LocOrg")
dict_PER_NAME = Use.open_dictionary("dict_PER_NAME")
dict_PER_SURNAME = Use.open_dictionary("dict_PER_SURNAME")
dict_PER_PATRONYMIC = Use.open_dictionary("dict_PER_PATRONYMIC")
dict_identificators_LOC = Use.open_dictionary("dict_identificators_LOC")
dict_identificators_PER = Use.open_dictionary("dict_identificators_PER")

dict_suffixes_ORG = Use.open_dictionary("dict_suffixes_ORG")
dict_parts_PERSON = Use.open_dictionary("dict_parts_PERSON")
dict_ADJ_GEO = Use.open_dictionary("dict_ADJ_GEO")
dict_NAMES_chinese = Use.open_dictionary("dict_NAMES_chinese")
dict_suffixes_PERSON = Use.open_dictionary("dict_suffixes_PERSON")
dict_parts_ORG = Use.open_dictionary("dict_parts_ORG")
dict_VERBS_SPEECH = Use.open_dictionary("dict_VERBS_SPEECH")
dict_PERSON = Use.open_dictionary("dict_PERSON")




def create_indexed_text(user_text, start_position = 0):
    """Функция возвращает проиндексированный текст.
    Args:
        user_text(str): текст предназначенный для индексации
        start_position(int): индекс первого символа в тексте; по умолчанию  равен 0
    Returns:
        list:список списков вида:
        [0](str): слово или символ пунктуации
        [1](int): индекс начала слова или символа пунктуации
        [2](int): длина
        [3](str): "тип" - word/punct/whitespace

    """
    punct = set([' ', ',', '.', ':', '?', '!', ';', '—', '(', ')','[',']','«','»','…','"',"'", '>', '^','$','%', '<','=','/','\'','|'])
    whitespace = set([' ','\n'])
    indexed_text = []
    in_word = False
    current_index = start_position
    current_word = ''
    # просматириваем строку посимвольно
    for char in user_text:
        # если символ-пунктуация
        if char in punct:
            # eсли до этого было слово, помещаем его в список
            if len(current_word) != 0:
                indexed_text.append({'token': current_word,'index':current_index-len(current_word),'length': len(current_word), 'token_type': 'word'})
                current_word = ''
            in_word = False
            # если у нас whitespace
            if char in whitespace:
                indexed_text.append({'token': char, 'index': current_index, 'length': 1, 'token_type': 'whitespace'})
                current_index += 1
            # добавляем пунктуацию в список

            else:
                indexed_text.append({'token': char, 'index': current_index, 'length': 1,'token_type': 'punct'})
                current_index += 1
        # если мы внутри слова
        elif in_word:
            # добавлем символ в слово
            current_word += char
            current_index += 1
        # слово началось на этом символе
        else:
            in_word = True
            current_word += char
            current_index += 1

    return indexed_text


def change_quotes(text):
    text_with_changed_quotes = []
    for token in text:
        if token['token'] == "«" or token['token'] == '»':
            token['token'] = '"'
            text_with_changed_quotes.append(token)
        else:
            text_with_changed_quotes.append(token)
    return text_with_changed_quotes


def delete_whitespaces(text):
    result = []
    for token in text:
        if token['token_type'] != 'whitespace':
            result.append(token)
    return result



def lemmatize(indexed_text):
    """
    Функция добавляет к каждому слову его лемму.
    :param indexed_text: на вход подаётся индексированный текст
    :return: возвращает изначальный индексированный список, к каждой строке добавляется лемма слова
    """
    for token in indexed_text:
        if token['token_type'] != 'punct' and token['token_type'] != 'whitespace':
            lemma = m.lemmatize(token['token'])
            token['lemma'] = ''.join(lemma).strip()
        else:
            token['lemma'] = 'none'
    return indexed_text


def analyze(indexed_text):
    """
    Функция выводит морфологические характеристики каждого токена в тексте. Для морфологического анализа используется
    модуль Mystem.
    :param indexed_text: на вход подаётся индексированный текст
    :return: возвращает изначальный индексированный текст, в каждый токен записывается ключ "analysis" со значением
    грамматической информации
    """
    for token in indexed_text:
        if token['token_type'] == 'word':
            try:
                token['analysis'] = m.analyze(token['token'])[0]['analysis'][0]['gr']
            except:
                token['analysis'] = 'none'
                pass
        else:
            token['analysis'] = 'none'
    return indexed_text



def contains_digits(token):
    # Вспомогательная функция для анализа формы слова# Вспомогательная функция для анализа формы слова
    if token.isdigit():
        return 'is_digit'
    else:
        digits = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
        for letter in token:
            if letter in digits:
                return "contains_digits"
            else:
                return 'none'


def alphabet(word):
    # Вспомогательная функция для анализа формы слова# Вспомогательная функция для анализа формы слова
    latin = 0
    cyrillic = 0
    for letter in word.lower():
        if letter in 'abcdefghijklmnopqrstuvwxyz':
            latin += 1
        elif letter in 'абвгдежзийклмнопрстуфхцчшщъыбэюя':
            cyrillic += 1
    if latin > 0 and cyrillic == 0:
        return "latin"
    elif latin > 0 and cyrillic > 0:
        return "mixed"
    else:
        return "cyrillic"


def mixed_case(word):
    # Вспомогательная функция для анализа формы слова
    if len(word) > 2:
        count_upper = 0
        count_lower = 0
        for letter in word:
            if letter.isupper():
                count_upper += 1
            elif letter.lower():
                count_lower += 1
        if count_upper >= 2 and count_lower >= 1:
            return "mixed"
        else:
            return 'none'


def shape(word):
    # Вспомогательная функция для анализа формы слова# Вспомогательная функция для анализа формы слова
    if word[0].isupper() and word[1:].islower():
        return 'capitalized'
    elif word.isupper():
        return 'upper'
    elif word.islower():
        return 'lower'
    elif mixed_case(word):
        return 'mixed'
    else:
        return 'none'


def hyphen(token):
    # Вспомогательная функция для анализа формы слова# Вспомогательная функция для анализа формы слова
    if '-' in token:
        return 'contains_hyphen'
    else:
        return 'none'


def spelling(indexed_text):
    """
    Функция возвращает текст, в котором для каждого слова указан тип его написания (orthography).

    :param indexed_text: на вход подаётся текст, проиндексированный с помощью функции create_indexed_text(user_text)
    :return: возвращает изначальный проиндексированный текст, к каждой строке добавляются значения следующих фичей:

    фича shape:
    "capitalized" - если первая буква слова прописная
    "upper" - если слово написано прописными буквами
    "mixed_case" - если слово написано сЛеДуюЩим ОБРазом

    фича digits:
    "contains_digits" - для слов содержащих цифры
    "is_digit" - для слов, содержащих только цифры

    фича hyphen
    "contains_hyphen" - для слов с дефисным написанием

    фича alphabet
    "contains_latin" - для слов, содержащих латиницу
    "mixed_case" - для слов, содержащий и латиницу, и кириллицу

    если токен не содержит признака или является знаком препинания, ему присваивается значение None
    """

    for token in indexed_text:
        if token['token_type'] != 'punct' and token['token_type'] != 'whitespace':
            token['shape'] = shape(token['token'])
            token['digits'] = contains_digits(token['token'])
            token['alphabet'] = alphabet(token['token'])
            token['hyphen'] = hyphen(token['token'])
        else:
            token['shape'] = 'none'
            token['digits'] = 'none'
            token['alphabet'] = 'none'
            token['hyphen'] = 'none'
    return indexed_text


def initialize_dict(text):
    for token in text:
        token['dict'] = []
    return text


def is_in_dictionary(indexed_text, dict_name='dict_PER_NAME', label='dict=PER'):
    """
    Функция проверяет для всех токенов текста наличие в словаре.
    :param indexed_text: проиндексированный текст;
    :param dict_name: имя словаря; по умолчанию стоит словарь персон (имена);
    :param label: аннотация, которую мы добавляем к токену;
    :return: возвращает индексированный текст
    """
    dictionary = dict_name
    for token in indexed_text:
        if token['token_type'] != 'punct' and token['token_type'] != 'whitespace' and len(token['token']) > 1:
            if token['lemma'] in dictionary:
                if 'dict' in token:
                    token['dict'].append(label)
                else:
                    token['dict'] = [label]
    return indexed_text


def identificator(text, dict_name="dict_identificators_PER",label="ident=PER"):
    dictionary = Use.open_dictionary(dict_name)
    for token in text:
        if token['lemma'] in dictionary:
            token['dict'].append(label)
    return text


def geo_adjectives(indexed_text):
    for token in indexed_text:
        if token['token_type'] != 'punct' and token['token_type'] != 'whitespace' and token['analysis']:
            if "гео" in token['analysis'] and ("A=" in token['analysis'] or "A," in token['analysis']):
                if 'dict' in token:
                    token['dict'].append('GEO_ADJ')
                else:
                    token['dict'] = ['GEO_ADJ']
    return indexed_text


def contains_suffix(indexed_text, dict_name):
    dictionary = dict_name
    for line in indexed_text:
        count = 0
        if line[3] != 'punct':
            for suffix in dictionary:
                if line[4].endswith(suffix) and len(line[4]) > len(suffix):
                    count += 1

            if count > 0:
                line.append('suffix=' + dict_name[14:])
    return indexed_text


def no_whitespaces(indexed_text):
    result = []
    for token in indexed_text:
        if token['token_type'] != 'whitespace':
            result.append(token)
    return result


def suffix(text, dict_name=dict_suffixes_PERSON, label='suffix=PERSON'):
    d = dict_name
    for token in text:
        for suffix in d:
            if token['lemma'].endswith(suffix) and token['shape'] == 'capitalized':
                token['dict'].append(label)
    return text


def parts(text, dict_name=dict_parts_ORG, label='part=ORG'):
    d = dict_name
    for token in text:
        for part in d:
            if part in token['lemma'] and token['shape'] != 'lower':
                token['dict'].append(label)
    return text


def verb_of_speech(text, dict_name=dict_VERBS_SPEECH, label='speech_verb'):
    d = dict_name
    for token in text:
        if token['lemma'] in d:
            token['dict'].append(label)
    return text

def chinese_name(text):
    d = dict_NAMES_chinese
    for token in text:
        if token['token'].lower() in d:
            token['dict'].append("asian_name")
    return text

def pipeline(filename):

    text = Use.open_file(filename)
    print("Предобработка текста...")
    # индексируем
    text = create_indexed_text(text)
    text = delete_whitespaces(text)
    text = change_quotes(text)
    # лемматизируем
    text = lemmatize(text)
    text = spelling(text)

    text = initialize_dict(text)

    # дескрипторы
    print("Поиск в словарях...")
    text = is_in_dictionary(text, dict_name=dict_descriptors_LOC, label='descr=LOC')
    text = is_in_dictionary(text, dict_name=dict_descriptors_ORG, label='descr=ORG')
    text = is_in_dictionary(text, dict_name=dict_descriptors_ORG_PER, label='descr=ORG_PER')
    text = is_in_dictionary(text, dict_name=dict_LOC, label='LOC')
    text = is_in_dictionary(text, dict_name=dict_LocOrg, label="LocOrg")

    text = is_in_dictionary(text, dict_name=dict_PER_NAMES_popular, label='popular_name')


    # Имя, фамилия, отчество
    text = is_in_dictionary(text, dict_name=dict_PER_NAME, label='dict=PER_NAME')
    text = is_in_dictionary(text, dict_name=dict_PER_SURNAME, label='dict=PER_SURNAME')
    text = is_in_dictionary(text, dict_name=dict_PER_PATRONYMIC, label='patronymic')

    # Размечаем
    text = is_in_dictionary(text, dict_name=dict_identificators_LOC, label='ident=LOC')
    text = is_in_dictionary(text, dict_name=dict_identificators_PER, label='ident=PER')
    text = identificator(text)
    text = chinese_name(text)

    text = suffix(text)
    text = suffix(text, dict_name=dict_suffixes_ORG, label='suffix=ORG')
    text = parts(text)
    text = parts(text, dict_name=dict_parts_PERSON, label='part=PER')
    text = verb_of_speech(text)


    # Геоприлагательные
    text = analyze(text)
    text = geo_adjectives(text)
    text = is_in_dictionary(text,dict_name=dict_ADJ_GEO, label="GEO_ADJ")

    # Коллокации
    print("Поиск коллокаций...")
    text = Ng.search_all_collocations(text)
    text = Ng.search_all_collocations(text, dict_name="dict_LOC", label="LOC")
    text = Ng.search_all_collocations(text, dict_name="dict_PERSON", label="PER")

    # text = Ng.search_collocations(text, dict_name="dict_LocOrg", n=2, label="LocOrg")
    # text = Ng.search_collocations(text, dict_name="dict_LocOrg", n=3, label="LocOrg")

    # Use.write_in_file(text, filename + '_features')

    return text


# text = pipeline('example2')
# pprint.pprint(text, width=3)
