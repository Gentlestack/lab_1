# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import zipfile
import hashlib
import requests
from bs4 import BeautifulSoup
import re

directory_to_extract_to = 'C:\\Lab_3'     # директория извлечения файлов архива
arch_file = 'C:\\Downloads\\tiff-4.2.0_lab1.zip'  # путь к архиву

test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall(directory_to_extract_to)

sh_files = []
for r, d, f in os.walk(directory_to_extract_to):
    # print("it is r: ", r)
    # print("it is d: ", d)
    # print("it is f: ", f)
    for i in f:
        if i.endswith('.sh'):
            target_file = (r+"\\"+i)
            target_file_data = open(target_file, 'rb').read()
            result = hashlib.md5(target_file_data).hexdigest()
            # print(target_file, "\t", result)
            sh_files.append(target_file)
            sh_files.append(result)
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
for x, i in enumerate(sh_files):
    if i == target_hash:
        target_file = sh_files[x-1]
        target_file_data = open(target_file, 'rb').read()
        print(target_file)
        print(target_file_data)
# print(sh_files)

r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

# info = rq.get(link)
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)

counter = 0
for line in lines:
    if counter == 0:
        headers = re.sub(r"<.*?>", " ", line)
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
        print(headers)
        counter = 1
    else:
        cleanLine = re.sub(r"<.*?>", " ", line)
        data = re.sub(r"\(.*?\)", "", cleanLine)
        data = re.sub(r"\*", "", data)
        data = re.sub(r"_ ", "-1", data)
        data = re.sub(r"\xa0", "", data)
        splitData = re.split(r' {2,4}', data)
        country_name = splitData[2]
        # data = re.findall("\(.*?\)", line)
        result_dct[country_name] = {}
        result_dct[country_name][headers[0]] = int(splitData[3])
        result_dct[country_name][headers[1]] = int(splitData[4])
        result_dct[country_name][headers[2]] = int(splitData[5])
        result_dct[country_name][headers[3]] = int(splitData[6])
        # data = re.findall()
        # print(splitData)
output = open('data.csv', 'w')
for key in result_dct.keys():
    output.write(key)
    output.write(';')
    output.write(str(result_dct[key][headers[0]]))
    output.write(';')
    output.write(str(result_dct[key][headers[1]]))
    output.write(';')
    output.write(str(result_dct[key][headers[2]]))
    output.write(';')
    output.write(str(result_dct[key][headers[3]]))
    output.write('\n')
output.close()

target_country = input("Введите название страны: ")
print(result_dct[target_country][headers[0]])

# soup = BeautifulSoup(r.text, 'lxml')
# print(soup)

# quotes = soup.find_all('div', class_='Table-module_row__3TH83')
# cells = soup.find_all('div', class_='Table-module_cell__EFKDW Table-module_white__gzvo0 Table-module_s__Vl_Eg')
# lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
# for quote in cells:
    # if counter == 0:
        # headers = quote.text
        # pattern = re.sub('\(.*?\)', '', headers)
        # print(pattern)

    # if pattern!=[]:
        # a.replace(str(pattern[0]), '')
        # print(a)
    # if pattern != None:
        # re.sub(r'\(\+?.*\)', ..., a)

    # print(quote.text.find('('))
    # print(quote.text.find('('))
    # print(a)
# print(quotes)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
