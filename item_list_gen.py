import urllib.request, json
from unidecode import unidecode
from pathlib import Path

with urllib.request.urlopen("https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json") as url:
    item_list = json.load(url)

item_dict = {}

for i in range(len(item_list)-1):
    try:
        encantamentos = [f"@{i+1}" for i in range(4)]
        for j in encantamentos:
            if j in item_list[i]['UniqueName']:
                item_list[i]['UniqueName'] = item_list[i]['UniqueName'].replace(j,'')
        item_dict[unidecode(item_list[i]['LocalizedNames']['PT-BR']).lower()] = item_list[i]['UniqueName']
        item_dict[item_list[i]['LocalizedNames']['EN-US'].lower()] = item_list[i]['UniqueName']
    except:
        pass

with open(f'{Path.home()}\\Downloads//item_list.json', 'w+') as fp:
    json.dump(item_dict, fp, indent=4)
