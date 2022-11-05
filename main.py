import urllib.request, json

cities ='''
Lymhurst
Bridgewatch
FortSterling
Martlock,
Thetford
Caerleon
'''.replace('\n','')

quality_dict = {
    '0': 'All',
    '1': 'Normal',
    '2': 'Good',
    '3': 'Outstanding',
    '4': 'Excellent',
    '5': 'Masterpiece',
}

def color_func(city):
    if 'Lymhurst' in city:
        return f"\033[92m{city}\033[0m"
    
    elif 'Bridgewatch' in city:
        return f"\033[93m{city}\033[0m"
    
    elif 'Fort Sterling' in city:
        return f"\033[1m{city}\033[0m"
    
    elif 'Martlock' in city:
        return f"\033[94m{city}\033[0m"
    
    elif 'Thetford' in city:
        return f"\033[95m{city}\033[0m"
    
    elif city in ['Caerleon', 'Black Market']:
        return f"\033[91m{city}\033[0m"
    else:
        return f"\033[36m{city}\033[0m"

def enchantment_func(enchantment_num):
        match enchantment_num:
            case '0':
                print()
                return ''
            case _:
                return f'@{enchantment_num}'

def data_func(timestamp):
    return f'{timestamp[8:10]}/{timestamp[5:7]}/{timestamp[0:4]} / {timestamp[11:13]}:{timestamp[14:16]}:{timestamp[17:20]}'

def search(item,quality,enchantment):
    try:
        with open('item_list.json' , 'r') as fp:
            item_list = json.load(fp)
    except:
        print('[!] Arquivo JSON não encontrado!\n')
        return 0


    try:
        url = f"https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}{enchantment_func(enchantment)}?locations={cities}&qualities={quality}"
        with urllib.request.urlopen(url) as url_obj:
            data = json.load(url_obj)
    except:
        print(f'[!] {item.title()} não existe!\n')


    try:
        print(f"\n[+] Procurando por: {item.title()} | Qualidade: {quality_dict[quality]}")
        
        def quality_func(quality_num):
            match quality_num:
                case '0':
                    return f" Qualidade: {quality_dict[str(data[i]['quality'])]}"
                case _:
                    return ''

        for i in range(len(data)):
            try:
                if data[i]['sell_price_min'] != 0:
                    print(f"[=] {color_func(data[i]['city'])}: ${data[i]['sell_price_min']:,} |{quality_func(quality)} ({data_func(data[i]['sell_price_min_date'])})")
            except Exception as err:
                print('[!]',err)
        print('')
    except:
        print(f'[!] Busca inválida\n')
        return 0


while __name__ == '__main__':
    search(input('[+] Digite o nome do item para buscar: '),input('[+] Digite o número da qualidade desejada (0/1/2/3/4/5): '),input('[+] Digite o número do encantamento do item (0/1/2/3): '))
