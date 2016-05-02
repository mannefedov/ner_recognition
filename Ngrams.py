# -*- coding: utf-8 -*-
import codecs
import collections
import Useful_functions as Use
from pymystem3 import Mystem
m = Mystem()


def next_token(text, current_token):
    current_index = text.index(current_token)
    return text[current_index + 1]


def previous_token(text, current_token):
    current_index = text.index(current_token)
    return text[current_index - 1]


def collocations(text, n=2):
    collocations_list = []
    for token in text[:-2]:
        if token['token_type'] == 'word':
            i = 0
            current_token = token
            collocation = [token['lemma']]

            while i < n-1:
                nt = next_token(text, current_token)
                if nt['token_type'] == 'punct':
                    collocation = None
                    break
                else:
                    if nt['lemma']:
                        collocation.append(nt['lemma'])
                current_token = nt
                i += 1
            if collocation:
                collocations_list.append(collocation)

    return collocations_list


def search_collocations(text, n=2, dict_name="dict_ORG_2", label="ORG"):
    dictionary = Use.open_dictionary(dict_name)
    for token in text[:-n]:
        if token['token_type'] == 'word':
            i = 0
            current_token = token
            collocation = [token['lemma']]

            while i < n-1:
                nt = next_token(text, current_token)
                if nt['token_type'] == 'punct':
                    collocation = None
                    break
                else:
                    if nt['lemma']:
                        collocation.append(nt['lemma'])
                current_token = nt
                i += 1
            if collocation:
                if ' '.join(collocation) in dictionary:
                    current_token = token
                    current_index = text.index(token)
                    text[current_index]['dict'].append(label + '_B')
                    i = 0
                    while i < n-1:
                        current_token = next_token(text, current_token)
                        current_index = text.index(current_token)
                        text[current_index]['dict'].append(label + '_I')
                        i += 1

    return text


def partial_search(text, collocation, label="collocation", rule="partial_search_rule", c_type="list"):
    if c_type == "list":
        for token in text[:-len(collocation)]:
            if ("org_by_dict" not in token['rules'] and "org_by_descr_rule" not in token['rules'] and
                        "person_by_dict" not in token['rules'] and "popular_name_rule" not in token['rules']):
                test = True
                i = 0
                current_token = token
                while i < len(collocation):
                    if current_token['lemma'] == collocation[i]:
                        test = True
                        i += 1
                        current_token = next_token(text, current_token)
                    else:
                        test = False
                        break
                if test:
                    token["rules"].update({rule: label + "_B"})
                    current_token = token
                    i = 1
                    while i < len(collocation):
                        current_token = next_token(text, current_token)
                        current_index = text.index(current_token)
                        text[current_index]["rules"].update({rule: label + "_I"})
                        i += 1
    elif c_type == 'string':
        for token in text:
            if ("org_by_dict" not in token['rules'] and "org_by_descr_rule" not in token['rules'] and
                        "person_by_dict" not in token['rules'] and "popular_name_rule" not in token['rules']):
                if token['lemma'] == collocation and token['shape'] == 'capitalized':
                    token['rules'].update({rule: label + "_B"})
    return text



def search_all_collocations(text, dict_name="dict_ORG", label="ORG"):
    text = search_collocations(text, n=1, dict_name=dict_name + '_1', label=label)
    text = search_collocations(text, n=2, dict_name=dict_name + '_2', label=label)
    text = search_collocations(text, n=3, dict_name=dict_name + '_3', label=label)
    text = search_collocations(text, n=4, dict_name=dict_name + '_4', label=label)
    text = search_collocations(text, n=5, dict_name=dict_name + '_5', label=label)
    text = search_collocations(text, n=6, dict_name=dict_name + '_6', label=label)
    # text = search_collocations(text, n=8, dict_name=dict_name + '_6', label=label)
    # text = search_collocations(text, n=9, dict_name=dict_name + '_6', label=label)


    return text



def check_references(text, word):
    for token in text:
        if token['lemma'] == word and token['shape'] == 'lower':
            return False
    return True
