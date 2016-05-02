import os
import codecs
import Basic_Features as Bf
import Extracting_Rules as Rules
import Useful_functions as Use
import Json_Handler as Jh

# Путь, где лежит коллекция текстов для соревнований
os.chdir('/Users/ulyanasidorova/Downloads/XXX')

# Папка с результатами
path = '/Users/ulyanasidorova/Downloads/XXX'
try:
    os.mkdir(path)
except FileExistsError:
    pass


for filename in sorted(os.listdir(os.getcwd())):
    if not filename.split('.')[0].endswith('.'):
        f = codecs.open(filename, 'r')
        filename = filename.split('.')[0]
        print(filename)
        text = Bf.pipeline(filename)

        text = Rules.pipeline(text)

        result = Jh.formatting(text)
        for line in result:
            print(line)

        Use.write_as_object(result, filename, path=path)


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
