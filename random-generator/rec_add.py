# -*- coding: utf-8 -*-
import json
import random

names = open('names.json')
books = open('book.json')
csv_file = open('records.csv', 'w')

name_list = json.load(names)
book_list = json.load(books)

for i in range(999):
    a = random.randint(0, 999)
    title = book_list[a]["title"].strip().replace(',', '')
    lc = book_list[a]["lc"].strip().replace(',', '')
    b = random.randint(1, 3)
    writer_list = []
    for i in range(b):
        c = random.randint(0, 999)
        first_name = name_list[c]['first_name'].strip().replace(',', '')
        last_name = name_list[c]['last_name'].strip().replace(',', '')
        date = name_list[c]['date'].strip()
        writer_list.append("{},{},{}".format(first_name.title(), last_name.title(), date))
    csv_file.write(title.title() + ',' + lc + ',' + ','.join(writer_list) + '\n')
csv_file.close()
books.close()
names.close()
