import Useful_functions as Use
import Ngrams as Ng
import pprint

# text = Use.open_json('book_0_result', path='/Users/ulyanasidorova/Downloads/testset-old/result')


# result = []
# for token in text[:-1]:
#     print(token['lemma'])

def formatting(text):
    result = []
    for token in text[:-1]:
        rules = list(token['rules'].values())
        if "ORG_B" in rules:
            name = []
            name.append(token['token'])
            current_token = Ng.next_token(text, token)
            while True:
                try:
                    if "ORG_I" in list(current_token['rules'].values()):
                        name.append(current_token['token'])
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break
                except IndexError:
                    pass


            x = ' '.join(["ORG", str(token['index']), str(len(' '.join(name).strip()))]) + " " + ' '.join(name).strip()
            result.append(x)


        elif "PER_B" in rules:
            name = []
            name.append(token['token'])
            current_token = Ng.next_token(text, token)
            while True:
                try:


                    if "PER_I" in list(current_token['rules'].values()):
                        name.append(current_token['token'])
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break
                except IndexError:
                    pass

            x = ' '.join(["PER", str(token['index']), str(len(' '.join(name).strip()))]) + " "  + ' '.join(name).strip()
            result.append(x)


        elif "LOC_B" in rules:
            name = []
            name.append(token['token'])
            current_token = Ng.next_token(text, token)
            while True:
                try:
                    if "LOC_I" in list(current_token['rules'].values()):
                        name.append(current_token['token'])
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break
                except IndexError:
                    pass

            x = ' '.join(["LOC", str(token['index']), str(len(' '.join(name).strip()))]) + " "  + ' '.join(name).strip()
            result.append(x)

        if "LOC_ORG_B" in rules:
            name = []
            name.append(token['token'])
            current_token = Ng.next_token(text, token)
            while True:
                try:
                    if "LOC_ORG_I" in list(current_token['rules'].values()):
                        name.append(current_token['token'])
                        current_token = Ng.next_token(text, current_token)
                    else:
                        break
                except IndexError:
                    pass
            x = ' '.join(["LOCORG", str(token['index']), str(len(' '.join(name).strip()))]) + " "  + ' '.join(name).strip()
            result.append(x)

    return result

