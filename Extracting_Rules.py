# -*- coding: utf-8 -*-
import Useful_functions as Use
import Basic_Features as Bf
import Ngrams as Ng
import pprint
from pymystem3 import Mystem
m = Mystem()


def initialize_annotation(text):
    for token in text:
        token['rules'] = {}
    return text


def in_quotes(text, n=5):
    for token in text[1:-n]:
        if token['token'] == '"' and "quotation_B" not in token['dict'] and "quotation_I" not in Ng.previous_token(text, token)['dict']:
            i = 0
            current_token = token
            quoted_phrase = []
            while i != n:
                current_token = Ng.next_token(text, current_token)
                current_index = text.index(current_token)
                if current_token['token'] != '"':
                    quoted_phrase.append(current_index)
                else:
                    break
                i += 1
                if i == n:
                    quoted_phrase = []
            if quoted_phrase:
                text[quoted_phrase[0]]['dict'].append("quotation_B")
                for j in quoted_phrase[1:]:
                    text[j]['dict'].append("quotation_I")
    result = []
    for token in text:
        if token['token'] != '"':
            result.append(token)
    return result


def match_bank(text):
    for token in text[1:-1]:
        if token['lemma']:

            if token['lemma'].endswith("банк") and token['length'] > 4 and (token['shape'] == 'upper' or
            token['shape'] == 'capitalized'):
                token['rules'].update({"org_bank_rule": "ORG_B"})

            elif token['lemma'] == "банк":
                next_token = Ng.next_token(text, token)
                next_index = text.index(next_token)
                previous_token = Ng.previous_token(text, token)
                previous_index = text.index(previous_token)

                if "ADJ_ORG_bank" in previous_token['dict']:
                    token['rules'].update({"org_bank_rule:" "ORG_I"})
                    text[previous_index]['rules'].update({"org_bank_rule": "ORG_B"})
                elif token['shape'] == 'capitalized' and (next_token['shape'] != 'normal' or next_token['alphabet'] != "cyrillic"):
                    token['rules'].update({"org_bank_rule": "ORG_B"})
                    text[next_index]['rules'].update({"org_bank_rule": "ORG_I"})

    return text


# Организации

def loc_org(text):
    for token in text[1:-1]:
        next_token = Ng.next_token(text, token)
        previous_token = Ng.previous_token(text, token)
        next_index = text.index(next_token)
        previous_index = text.index(previous_token)
        if "LocOrg" in token['dict'] and "LOC_B" in next_token['dict']:
            token['rules'].update({"loc_org_rule": "LOC_ORG_B"})
            text[next_index]['rules'].update({"loc_org_rule": "LOC_ORG_I"})
        elif "LocOrg" in token['dict'] and "GEO_ADJ" in previous_token['dict']:
            token['rules'].update({"loc_org_rule": "LOC_ORG_I"})
            text[previous_index]['rules'].update({"loc_org_rule": "LOC_ORG_B"})
    return text


def org_by_descriptor(text):
    for token in text[1:-1]:
        next_token = Ng.next_token(text, token)
        next_index = text.index(next_token)

        # Размечаем паттерн "дескриптор" + последующие токены в кавычках
        if "descr=ORG" in token['dict']:
            if "quotation_B" in next_token['dict']:
                text[next_index]['rules'].update({"org_by_descr_rule": "ORG_B"})
                # token['rules'].update({"org_by_descr_rule": "ORG_B"})
                current_token = Ng.next_token(text, next_token)
                while True:
                    if "quotation_I" in current_token['dict']:
                        current_index = text.index(current_token)
                        text[current_index]['rules'].update({"org_by_descr_rule": "ORG_I"})
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break

            elif "ORG_B" in next_token['dict'] and next_token['shape'] != 'lower':
                # token['rules'].update({"org_by_descr_rule": "ORG_B"})
                text[next_index]['rules'].update({"org_by_descr_rule": "ORG_B"})
                current_token = Ng.next_token(text, next_token)
                while True:
                    if "ORG_I" in current_token and current_token['shape'] != 'lower':
                        current_index = text.index(current_token)
                        text[current_index]['rules'].update({"org_by_descr_rule": "ORG_I"})
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break

            elif (next_token['alphabet'] != "cyrillic" or next_token['digits'] == 'contains_digits') and next_token['shape'] != "lower":
                current_token = Ng.next_token(text, token)
                test = False
                while True:
                    if current_token['token_type'] == 'word':
                        if (current_token['alphabet'] != "cyrillic" or current_token['digits'] == 'contains_digits') and current_token['shape'] != "lower":
                            current_index = text.index(current_token)
                            text[current_index]['rules'].update({"org_by_descr_rule": "ORG_I"})
                            current_token = Ng.next_token(text, current_token)
                            test = True
                        else:
                            test = False
                            break
                    else:
                        test = False
                        break
                # if test:
                #     token['rules'].update({"org_by_descr_rule": "ORG_B"})
    return text


def org_by_shape(text):
    for token in text:
        if token['shape'] != 'lower' and ('suffix=ORG' in token['dict'] or 'part=ORG' in token['dict']):
            token['rules'].update({"org_by_shape"})



def org_by_quotes(text):
    for token in text:
        if "quotation_B" in token['dict'] and token['shape'] != 'lower' and ("ORG_B" in token['dict'] or
                                                                                     'suffix=ORG' in token['dict']):
            # token['rules'].update({"org_by_quotes": "ORG_I"})
            token['rules'].update({"org_by_quotes": "ORG_B"})
            current_token = Ng.next_token(text, token)
            while True:
                if "quotation_I" in current_token['dict']:
                    current_index = text.index(current_token)
                    text[current_index]['rules'].update({"org_by_quotes": "ORG_I"})
                    current_token = Ng.next_token(text, current_token)
                else:
                    break
    return text


def org_by_person_descriptor(text):
    for token in text[:-1]:
        if "descr=PER" in token['dict']:
            next_token = Ng.next_token(text, token)
            next_index = text.index(next_token)


            if "quotation_B" in next_token['dict']:
                text[next_index]['rules'].update({"org_by_person_descr_rule": "ORG_I"})
                token['rules'].update({"org_by_person_descr_rule": "ORG_B"})
                current_token = Ng.next_token(text, next_token)
                while True:
                    if "quotation_I" in current_token['dict']:
                        current_index = text.index(current_token)
                        text[current_index]['rules'].update({"org_by_person_descr_rule": "ORG_I"})
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break

            elif "ORG_B" in next_token['dict']:
                token['rules'].update({"org_by_person_descr_rule": "ORG_B"})
                text[next_index]['rules'].update({"org_by_person_descr_rule": "ORG_I"})
                current_token = Ng.next_token(text, next_token)
                while True:
                    if "ORG_I" in current_token:
                        current_index = text.index(current_token)
                        text[current_index]['rules'].update({"org_by_person_descr_rule": "ORG_I"})
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break

            elif ((next_token['alphabet'] != "cyrillic" or next_token['digits'] == 'contains_digits' or
                           'part=ORG' in token['dict'] or 'suffix=ORG' in token['dict']) and
                          next_token['shape'] != "lower"):
                current_token = Ng.next_token(text, token)
                test = False
                while True:
                    if current_token['token_type'] == 'word':
                        if (current_token['alphabet'] != "cyrillic" or current_token['digits'] == 'contains_digits') and current_token['shape'] != "lower":
                            current_index = text.index(current_token)
                            text[current_index]['rules'].update({"org_by_person_descr_rule": "ORG_I"})
                            current_token = Ng.next_token(text, current_token)
                            test = True
                        else:
                            test = False
                            break
                    else:
                        test = False
                        break
                if test:
                    token['rules'].update({"org_by_person_descr_rule": "ORG_B"})
    return text


def org_second_match(text):
    collocations_list = list()
    for token in text:

        # Если к токену применялось правило, использующее дескрипторы:
        if (('org_by_descr_rule' in token['rules'] and token['rules']['org_by_descr_rule'] == 'ORG_B') or
                ('org_by_person_descr_rule' in token['rules'] and
                         token['rules']['org_by_person_descr_rule'] == 'ORG_B') and
            'loc_by_mystem' not in token['rules'] and 'loc_by_dict' not in token['rules']):
            current_token = Ng.next_token(text, token)
            collocation = list()

            # Накапливаем коллокации в списке коллокаций
            while True:
                if "ORG_I" in list(current_token['rules'].values()) and "org_partial_search" not in current_token['rules']:
                    collocation.append(current_token['lemma'])
                    current_token = Ng.next_token(text, current_token)
                else:
                    break
                if collocation:
                    collocations_list.append(collocation)

        # Если к токену применялось правило, использующее поиск в кавычках:
        if "org_by_quotes" in token['rules'] and token['rules']['org_by_quotes'] == "ORG_B":
            collocation = list()
            collocation.append(token['lemma'])
            current_token = Ng.next_token(text, token)

            while True:
                if "ORG_I" in list(current_token["rules"].values()) and "org_partial_search" not in current_token["rules"]:
                    collocation.append(current_token['lemma'])
                    current_token = Ng.next_token(text, current_token)
                else:
                    break
                if collocation:
                    collocations_list.append(collocation)

    # Ищем все коллокации в тексте и размечаем их
    for collocation in collocations_list:
        text = Ng.partial_search(text, collocation, label="ORG")

    return text


def org_by_dict(text):
    for token in text:
        if "ORG_B" in token["dict"] and token["shape"] != "lower":
            token["rules"].update({"org_by_dict": "ORG_B"})
            current_token = token
            while True:
                current_token = Ng.next_token(text, current_token)
                if "ORG_I" in current_token["dict"]:
                    current_index = text.index(current_token)
                    text[current_index]['rules'].update({"org_by_dict": "ORG_I"})
                else:
                    break
    return text


def org_by_verbs(text):
    for token in text[1:-1]:
        if 'speech_verb' in token['dict']:
            next_token = Ng.next_token(text, token)
            previous_token = Ng.previous_token(text, token)
            if next_token['shape'] == 'capitalized' and next_token['alphabet'] != "cyrillic":
                ind = text.index(next_token)
                text[ind]['rules'].update({"org_by_verb_rule": "ORG_B"})
                current_token = Ng.next_token(text, next_token)
                while True:
                    if current_token['shape'] == 'capitalized' and current_token['alphabet'] != "cyrillic":
                        ind = text.index(current_token)
                        text[ind]['rules'].update({"org_by_verb_rule": "ORG_I"})
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break
            if previous_token['shape'] == 'capitalized' and previous_token['alphabet'] != "cyrillic":
                ind = text.index(previous_token)
                text[ind]['rules'].update({"org_by_verb_rule": "ORG_B"})
                current_token = Ng.previous_token(text, previous_token)
                while True:
                    if current_token['shape'] == 'capitalized' and current_token['alphabet'] != "cyrillic":
                        ind = text.index(current_token)
                        text[ind]['rules'].update({"org_by_verb_rule": "ORG_I"})
                        current_token = Ng.previous_token(text, current_token)
                    else:
                        break
            elif next_token['shape'] == 'capitalized' and 'suffix=ORG' in next_token['dict']:
                ind = text.index(next_token)
                text[ind]['rules'].update({"org_by_verb_rule": "ORG_B"})
            elif previous_token['shape'] == 'capitalized' and 'part=ORG' in previous_token['dict']:
                ind = text.index(previous_token)
                text[ind]['rules'].update({"org_by_verb_rule": "ORG_B"})
    return text


# Локации
def loc_sea(text):
    for token in text[1:-1]:
        next_token = Ng.next_token(text, token)
        previous_token = Ng.previous_token(text, token)

        if token['lemma'] == 'море':
            if previous_token['shape'] == 'capitalized' and (previous_token['token'].endswith('во') or previous_token['token'].endswith('ое')):
                token['rules'].update({"loc_sea": "LOC_ORG_I"})
                previous_index = text.index(previous_token)
                text[previous_index]['rules'].update({"loc_sea": "LOC_ORG_B"})
            elif next_token['shape'] == 'capitalized':
                token['rules'].update({"loc_sea": "LOC_ORG_B"})
                next_index = text.index(next_token)
                text[next_index]['rules'].update({"loc_sea": "LOC_ORG_I"})
    return text

def loc_by_dict(text):
    for token in text:
        if token["shape"] == "capitalized" and "LOC_B" in token["dict"]:
            token["rules"].update({"loc_by_dict_rule": "LOC_B"})
            current_token = token
            while True:
                current_token = Ng.next_token(text, current_token)
                if "LOC_I" in current_token["dict"]:
                    current_index = text.index(current_token)
                    text[current_index]["rules"].update({"loc_by_dict_rule": "LOC_I"})
                else:
                    break
    return text


def loc_by_mystem(text):
    for token in text:
        if "popular_name_rule" not in token['rules'] and "person_by_dict" not in token['rules'] and "person_asian_name" not in token['rules']:
            try:
                if (token["shape"] == "capitalized" and "гео" in token["analysis"] and "S" in token["analysis"] and
                            token['lemma'] != 'за' and token['lemma'] != 'по' and token['lemma'] != 'реджеп'):
                    token["rules"].update({"loc_by_mystem": "LOC_B"})
                    current_token = token
                    while True:
                        current_token = Ng.next_token(text, current_token)
                        if current_token["shape"] == "capitalized" and "гео" in token["analysis"] and "S" in token["analysis"]:
                            current_index = text.index(current_token)
                            text[current_index]["rules"].update({"loc_by_mystem": "LOC_I"})
                        else:
                            break
            except IndexError:
                pass
    return text

# Исправить дескриптор
def loc_by_descriptor(text):
    for token in text[1:-1]:
        if 'GEO_ADJ' in token['dict'] and token['shape'] == 'capitalized':
            previous_token = Ng.previous_token(text, token)
            next_token = Ng.next_token(text, token)
            if 'descr=LOC' in previous_token['dict']:
                if (previous_token['lemma'] != "город" and previous_token['lemma'] != "городок" and
                            previous_token['lemma'] != "деревня" and previous_token['lemma'] != "деревушка"):
                    ind = text.index(previous_token)
                    text[ind]['rules'].update({'loc_by_descriptor_rule': "LOC_B"})
                    token['rules'].update({'loc_by_descriptor_rule': "LOC_I"})
                else:
                    token['rules'].update({'loc_by_descriptor_rule': "LOC_B"})
            elif 'descr=LOC' in next_token['dict']:
                ind = text.index(next_token)
                token['rules'].update({'loc_by_descriptor_rule': "LOC_B"})
                text[ind]['rules'].update({'loc_by_descriptor_rule': "LOC_I"})
    for token in text[1:-1]:
        if 'descr=LOC' in token['dict'] and 'loc_by_descriptor_rule' not in token['rules']:
            previous_token = Ng.previous_token(text, token)
            next_token = Ng.next_token(text, token)
            if 'LOC' in next_token['dict'] and next_token['shape'] == 'capitalized':
                # token['rules'].update({"loc_by_descriptor_rule": "LOC_B"})
                ind = text.index(next_token)
                text[ind]['rules'].update({"loc_by_descriptor_rule": "LOC_B"})
            elif "LOC" in previous_token['dict'] and previous_token['shape'] == 'capitalized':
                # token['rules'].update({"loc_by_descriptor_rule": "LOC_I"})
                ind = text.index(previous_token)
                text[ind]['rules'].update({"loc_by_descriptor_rule": "LOC_B"})

    return text


def theater(text):
    for token in text:
        if ((token['lemma'] == 'театр' or token['lemma'] == 'университет' or token['lemma'] == 'институт' or
                     token['lemma'] == 'завод' or token['lemma'] == 'комбинат')):
            try:
                previous_token = Ng.previous_token(text, token)
                if "GEO_ADJ" in previous_token['dict'] and previous_token['shape'] == 'capitalized':
                    token['rules'].update({"org_theater_rule": "ORG_I"})
                    ind = text.index(previous_token)
                    text[ind]['rules'].update({"org_theater_rule": "ORG_B"})
            except IndexError:
                pass
            try:
                previous_token2 = Ng.previous_token(text, previous_token)
                if "GEO_ADJ" in previous_token2['dict'] and previous_token2['shape'] == 'capitalized':
                    token['rules'].update({"org_theater_rule": "ORG_I"})
                    ind = text.index(previous_token)
                    text[ind]['rules'].update({"org_theater_rule": "ORG_I"})
                    ind = text.index(previous_token2)
                    text[ind]['rules'].update({"org_theater_rule": "ORG_B"})
            except IndexError:
                pass
            try:
                next_token = Ng.next_token(text, token)
                if next_token['lemma'] == 'имя':
                    current_token = next_token
                    while True:
                        current_token = Ng.next_token(text, current_token)
                        if (current_token['shape'] == "capitalized" and
                                    "PER_I" in list(token['rules'].values()) and "PER_B" in list(token['rules'].values())):
                            ind = text.index(current_token)
                            text[ind]['rules'].update({"org_theater_rule": "ORG_I"})
                        else:
                            break
            except IndexError:
                pass
    return text







# Персоны

# Разметить границы?
# # =====================
def person_by_mystem(text):
    for token in text:
        if "popular_name_rule" not in token['rules'] and "person_by_dict" not in token['rules'] and "person_asian_name" not in token['rules']:
            try:
                next_token = Ng.next_token(text, token)
                if "PER_B" not in list(token["rules"].values()) and "PER_I" not in list(token["rules"].values()):
                    if "имя" in token["analysis"] and token["shape"] == "capitalized":
                        if next_token["token_type"] == "word":
                            if "фам" in next_token["analysis"] and next_token["shape"] == "capitalized":
                                token['rules'].update({"per_by_mystem": "PER_B"})
                                next_index = text.index(next_token)
                                text[next_index]['rules'].update({"per_by_mystem": "PER_I"})
                    if 'фам' in token["analysis"] and token["shape"] == "capitalized":
                        if "имя" in next_token["analysis"] and next_token["shape"] == "capitalized":
                            token['rules'].update({"per_by_mystem": "PER_B"})
                            next_index = text.index(next_token)
                            text[next_index]['rules'].update({"per_by_mystem": "PER_I"})
            except IndexError:
                break
    return text
# =====================


def person_popular_name(text):
    for token in text:
        if "popular_name" in token['dict']:
            if Ng.check_references(text, token['lemma']):
                token['rules'].update({"popular_name_rule": "PER_B"})
                try:
                    next_token = Ng.next_token(text, token)
                    if next_token['shape'] == "capitalized":
                        next_index = text.index(next_token)
                        text[next_index]['rules'].update({"popular_name_rule": "PER_I"})
                except IndexError:
                    break
                try:
                    previous_token = Ng.previous_token(text, token)
                    if (previous_token['shape'] == "capitalized" and ("dict=PER_NAME" in token['dict'] or
                                                                              "dict=PER_SURNAME" in token['dict'])):
                        previous_index = text.index(previous_token)
                        text[previous_index]['rules'].update({"popular_name_rule": "PER_I"})
                except IndexError:
                    pass
    return text



def person_mystem_name_name(text):
    for token in text:
        try:
            if 'имя' in token['analysis'] and token['shape'] == 'capitalized':
                if 'имя' in Ng.next_token(text, token) and Ng.next_token(text, token)['shape'] == 'capitalized':
                    token['rules'].update({"person_mystem_name_rule": "PER_B"})
                    next_index = text.index(Ng.next_token(text, token))
                    text[next_index]['rules'].update({"person_mystem_name_rule": "PER_I"})
        except IndexError:
            break
    return text


def person_name_surname(text):
    for token in text:
        try:
            next_token = Ng.next_token(text, token)
            next_index = text.index(next_token)
            if 'dict=PER_NAME' in token['dict'] and 'dict=PER_SURNAME' in next_token and next_token['shape'] == 'capitalized' and token['shape'] == 'capitalized':
                token['rules'].update({"person_name_surname_rule": "PER_B"})
                text[next_index].update({"person_name_surname_rule": "PER_B"})
            elif "dict=PER_SURNAME" in token['dict'] and 'dict=PER_NAME' in next_token and next_token['shape'] == 'capitalized' and token['shape'] == 'capitalized':
                token['rules'].update({"person_name_surname_rule": "PER_B"})
                text[next_index].update({"person_name_surname_rule": "PER_B"})
        except IndexError:
            break
    return text


def person_by_dict(text):
    for token in text:
        if 'PER_B' in token['dict'] and token['shape'] == 'capitalized':
            token['rules'].update({"person_by_dict": "PER_B"})
            current_token = token
            while True:
                current_token = Ng.next_token(text, current_token)
                if ("PER_I" in current_token['dict'] and (current_token['shape'] == 'capitalized'
                                                          or "part=PER" in current_token['dict'])):
                    current_index = text.index(current_token)
                    text[current_index]['rules'].update({"person_by_dict": "PER_I"})
                else:
                    break
    return text


def person_asian_name(text):
    for token in text:
        if "person_asian_name" not in token['rules']:
            try:
                if ("asian_name" in token['dict'] and token['shape'] == 'capitalized'
                        and "person_asian_name" not in token['rules']):
                    next_token = Ng.next_token(text, token)
                    next_next_token = Ng.next_token(text, next_token)
                    if ("asian_name" in next_token['dict'] and next_token['shape'] == 'capitalized' and
                          "asian_name" in next_next_token['dict'] and next_next_token['shape'] == 'capitalized'):
                        ind = text.index(next_next_token)
                        text[ind]['rules'].update({"person_asian_name": "PER_I"})
                        ind = text.index(next_token)
                        text[ind]['rules'].update({"person_asian_name": "PER_I"})
                        token['rules'].update({"person_asian_name": "PER_B"})
                    elif ("asian_name" in next_token['dict'] and next_token['shape'] == 'capitalized' and
                                "person_asian_name" not in next_token['rules'] and
                                  "person_asian_name" not in token['rules']):
                        token['rules'].update({"person_asian_name": "PER_B"})
                        ind = text.index(next_token)
                        text[ind]['rules'].update({"person_asian_name": "PER_I"})
            except IndexError:
                pass
    return text


def person_partial_search(text):
    collocations_list = list()
    for token in text:
        if "person_asian_name" not in token['rules']:
            try:
                if (("person_by_mystem_rule" in token['rules'] and token['rules']['person_by_mystem_rule'] == 'PER_B') or
                        ("popular_name_rule" in token['rules'] and token['rules']['popular_name_rule'] == 'PER_B') or
                        ("person_mystem_name_rule" in token['rules'] and token['rules']['person_mystem_name_rule'] == 'PER_B')or
                        ("person_name_surname_rule" in token['rules'] and token['rules']["person_name_surname_rule"] == 'PER_B')):

                    current_token = Ng.next_token(text, token)
                    collocations_list.append(token['lemma'])
                    while True:
                        if "PER_I" in list(current_token['rules'].values()) and "person_partial_search" not in current_token['rules']:
                            collocations_list.append(current_token['lemma'])
                            current_token = Ng.next_token(text, current_token)
                        else:
                            break
            except IndexError:
                pass
        for collocation in collocations_list:
            # Чтобы не делать повторную разметку
            if ("person_by_mystem_rule" not in token['rules'] and "popular_name_rule" in token['rules'] and
                    "person_mystem_name_rule" not in token['rules'] and "person_name_surname_rule" not in token['rules']):

                text = Ng.partial_search(text, collocation, label="PER", c_type='string')

    return text


def person_patronymic(text):
    for token in text[1:-1]:
        if 'patronymic' in token['dict'] and token['shape'] == 'capitalized':
            next_token = Ng.next_token(text, token)
            previous_token = Ng.previous_token(text, token)
            if (('dict=PER_NAME' in previous_token['dict'] or "dict=PER_SURNAME" in previous_token['dict'] or
                         "PER_B" in previous_token['dict'] or "PER_I" in previous_token['dict']) and
                        previous_token['shape'] == 'capitalized'):
                token['rules'].update({'person_patronymic_rule': "PER_I"})
                ind = text.index(previous_token)
                text[ind]['rules'].update({'person_patronymic_rule': "PER_B"})
                if (('dict=PER_NAME' in next_token['dict'] or "dict=PER_SURNAME" in next_token['dict'] or
                            "PER_B" in next_token['dict'] or "PER_I" in next_token['dict']) and
                            previous_token['shape'] == 'capitalized'):
                    ind = text.index(next_token)
                    text[ind]['rules'].update({'person_patronymic_rule': "PER_I"})
    return text


def sud(text):
    for token in text[2:]:
        if token['lemma'] == 'суд':
            previous_token = Ng.previous_token(text, token)
            preprevious_token = Ng.previous_token(text, previous_token)
            if ((Ng.previous_token(text, token)['lemma'] == 'районный' or
                         Ng.previous_token(text, token)['lemma'] == 'районный') and
                        "GEO_ADJ" in preprevious_token['dict']):
                ind1 = text.index(preprevious_token)
                ind2 = text.index(previous_token)
                text[ind1]['rules'].update({"org_sud": "ORG_B"})
                text[ind2]['rules'].update({"org_sud": "ORG_I"})
                token['rules'].update({"org_sud": "ORG_I"})
    return text


def pipeline(text):
    # text = Use.open_json(filename, path)
    text = initialize_annotation(text)
    text = in_quotes(text, n=5)
    text = loc_org(text)
    text = match_bank(text)
    text = org_by_dict(text)
    text = org_by_quotes(text)
    text = org_by_descriptor(text)
    text = org_by_person_descriptor(text)
    text = org_by_verbs(text)
    text = org_second_match(text)
    text = theater(text)
    text = person_by_mystem(text)
    text = person_patronymic(text)
    text = person_asian_name(text)
    text = person_popular_name(text)
    text = person_name_surname(text)
    text = person_by_dict(text)
    text = person_partial_search(text)
    text = loc_by_dict(text)
    text = loc_sea(text)
    text = loc_by_descriptor(text)
    text = loc_by_mystem(text)

    return(text)



# for token in text:
#     if "LOC_B" in token['dict'] or "LOC_I" in token["dict"]:
#         print(token['token'], token['dict'])

# pprint.pprint(text, width=3)

# Создать промежуточный результат, в который будет записаны правила, детектнувшие токен, и тип, к которому может
# относиться сущность
# result = []
# for token in text:
#     if token['rules']:
#         result.append([{token["index"]: {"list_of_rules": list(token['rules'].keys()), "type": list(token['rules'].values())}, "token": token["token"], 'length': token['length']}])
# pprint.pprint(result)
# Use.write_as_json(result, "example2_rules")




# for token in text:
#     try:
#         if token['rules']:
#             if "ORG_B" in token['rules'][0].values() or "ORG_I" in token['rules'][0].values() or "LOC_B" in token['rules'][0].values() or "LOC_I" in token['rules'][0].values() or "LOC_ORG_B" in token['rules'][0].values() or "LOC_ORG_I" in token['rules'][0].values():
#                 name = token['token']
#                 test = True
#                 current_token = token
#                 while test:
#                     if "ORG_I" in Ng.next_token(text, current_token)['rules'][0].values() or "LOC_I" in Ng.next_token(text, current_token)['rules'][0].values() or "LOC_ORG_I" in Ng.next_token(text, current_token)['rules'][0].values():
#                         name = name + ' ' + Ng.next_token(text, current_token)['token']
#                         current_token = Ng.next_token(text, current_token)
#                         test = True
#                     else:
#                         test = False
#                 print("NE: ", token['index'], '#', name)
#     except IndexError:
#         print("THE END", token['token'])
#         pass
