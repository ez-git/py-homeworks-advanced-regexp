import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pattern = r'(\+7|8)+\s*\(?(\d\d\d)\)?[\s|-]?' \
          r'(\d\d\d)-?(\d\d)-?(\d\d)\s?\(?([доб.]*)\s?(\d+)*\)?'
re_pattern = re.compile(pattern)
replace = r'+7(\2)\3-\4-\5 \6\7'

for row_index in range(len(contacts_list)):
    row = contacts_list[row_index]
    if row_index > 0:
        fullname = f'{row[0]} {row[1]} {row[2]}'.split(' ')
        for fullname_index in range(3):
            row[fullname_index] = fullname[fullname_index]
        row[5] = re_pattern.sub(replace, row[5]).rstrip()
    row += [row_index]

key = lambda column: (column[0], column[1])
keys = set(map(key, contacts_list))
contacts_list = [
                    [
                        k[0],
                        k[1],
                        max(row[2] for row in contacts_list if k == key(row)),
                        max(row[3] for row in contacts_list if k == key(row)),
                        max(row[4] for row in contacts_list if k == key(row)),
                        max(row[5] for row in contacts_list if k == key(row)),
                        max(row[6] for row in contacts_list if k == key(row)),
                        next(row[7] for row in contacts_list if k == key(row))
                    ] for k in keys
                ]

contacts_list.sort(key=lambda i: i[len(contacts_list)-1])

for row in contacts_list:
    del row[-1]

with open("phonebook.csv", "w", encoding='windows-1251') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)