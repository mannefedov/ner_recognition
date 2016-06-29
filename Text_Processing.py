import os
import codecs
import Basic_Features as Bf
import Extracting_Rules as Rules
import Useful_functions as Use
import Json_Handler as Jh
from os.path import basename

# Путь, где лежит коллекция текстов для соревнований
input_path = './testset/'

# Папка с результатами
result_path = './result/'
try:
    os.mkdir(result_path)
except FileExistsError:
    pass

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
