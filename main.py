import os
import codecs
import Basic_Features as Bf
import Extracting_Rules as Rules
import Useful_functions as Use
import Json_Handler as Jh
from os.path import basename
import sys
import argparse


def createParser ():
    parser = argparse.ArgumentParser()
    # Путь, где лежит коллекция текстов для соревнований
    parser.add_argument ('-i', '--input', default='./texts/')
    # Папка с результатами
    parser.add_argument ('-o', '--output', default='./results/')
    return parser



if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    input_path = namespace.input + '/'* (not namespace.input.endswith('/'))
    result_path = namespace.output
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if os.path.exists(input_path):
    
        files = [input_path+file for file in  os.listdir(input_path)]

        for filename in sorted(files):
            try:
                if filename.endswith(".txt"):
                    f = codecs.open(filename, 'r')
                    #filename = filename.split('.')[0]
                    print("Обрабатывается файл", basename(filename))
                    text = Bf.pipeline(filename)
                    text = Rules.pipeline(text)

                    result = Jh.formatting(text)
                    for line in result:
                        print(line)

                    Use.write_as_object(result, basename(filename), path=result_path)
            except FileNotFoundError as err:
                print("Skipping 1 file", filename)
                pass
            except IsADirectoryError as err_2:
                pass
            except Exception as err_3:
                print(err_3)
                pass
    else:
        print('Папки "{}" не существует'.format(input_path))

# for filename in sorted(os.listdir(os.getcwd())):
#     if not filename.split('.')[0].endswith('features'):
#         try:
#             f = codecs.open(filename, 'r')
#             filename = filename.split('.')[0]
#             print(filename)
#             text = Bf.pipeline(filename)
#
#             text = Rules.pipeline(text)
#
#             result = Jh.formatting(text)
#             for line in result:
#                 print(line)
#
#             Use.write_as_object(result, filename, path=path)
#         except:
#             print("Skipping file " + filename)
#             pass
