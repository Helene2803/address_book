from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Поместить ФИО в поля lastname, firstname и surname.
new_contacts_list = []
new_contacts_list.append(contacts_list[0])
data = contacts_list[1:]

for d in data:
    name = ' '.join(d[:3]).strip()
    name = name.split(' ')
    for n in name:
        if n == '':
            name.remove(n)
    d[:3] = name

# Объединить все дублирующиеся записи в одну.
merged_notes = {}

for item in data:
    name = ' '.join(item[:3]).strip()
    if len(name.split(' ')) == 3:
        merged_notes[name] = item[3:]

for key, value in merged_notes.items():
    for item in data:
        if key == ' '.join(item[:3]) or ' '.join(item[:2]) in key:
            for i in item[3:]:
                if i not in value and i != '':
                    merged_notes[key].append(i)

for key, value in merged_notes.items():
        merged_notes[key] = [i for i in merged_notes[key] if i != '']

for key in merged_notes.keys():
    new_contacts_list.append(key.split(' '))

for i, value in enumerate(merged_notes.values(), 1):
    new_contacts_list[i].extend(value)

# Привести телефоны в единый формат и заменить их в итоговом списке.
for i, phone in enumerate(new_contacts_list):
    phone_pattern = r'(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})-?(\d{2})-?(\d{2})(\(?(доб\.)\s(\d{4})\)?)?'
    repl_pattern = r'+7(\2)\3-\4-\5'
    extension_num_pattern = r'\(?(доб\.)\s(\d{4})\)?'
    extension_repl_pattern = r'\1\2'
    for idx in range(len(phone)):
        if phone_pattern:
            cleaned_phone = re.sub(phone_pattern, repl_pattern, phone[idx])
            cleaned_extension_num = re.sub(extension_num_pattern, extension_repl_pattern, cleaned_phone)
            new_contacts_list[i][idx] = cleaned_extension_num

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(new_contacts_list)