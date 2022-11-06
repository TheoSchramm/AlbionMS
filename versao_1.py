import urllib.request, json

quality_dict = {
    '0': 'Qualquer',
    '1': 'Normal',
    '2': 'Boa',
    '3': 'Excepcional',
    '4': 'Excelente',
    '5': 'Obra-prima',
}

def enchantment_func(enchantment_num):
        match enchantment_num:
            case '0':
                print()
                return ''
            case _:
                return f'@{enchantment_num}'

def data_func(timestamp):
    return f'{timestamp[8:10]}/{timestamp[5:7]}/{timestamp[0:4]} / {timestamp[11:13]}:{timestamp[14:16]}:{timestamp[17:20]}'

def search():
    item = input('[+] Digite o nome do item para buscar: ')
    quality = input('[+] Digite o número da qualidade desejada (0/1/2/3/4/5): ')
    enchantment = input('[+] Digite o número do encantamento do item (0/1/2/3): ')
    
    try:
        with open('item_list.json' , 'r') as fp:
            item_list = json.load(fp)
    except:
        print('[!] Arquivo JSON não encontrado.\n')
        return 0

    
    try:
        url = f"https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}{enchantment_func(enchantment)}?locations=LymhurstBridgewatchFortSterlingMartlock,ThetfordCaerleon&qualities={quality}"
        with urllib.request.urlopen(url) as url_obj:
            data = json.load(url_obj)
    except:
        print(f'[!] {item.title()} não existe.\n')
        return 0

    
    try:
        print(f"\n[+] Procurando por: {item.title()} | Qualidade: {quality_dict[quality]}")
        search = 0
        for i in range(len(data)):
            if data[i]['sell_price_min'] != 0:
                search += 1
                print(f"[{search}] {data[i]['city']}: ${data[i]['sell_price_min']:,} | ({data_func(data[i]['sell_price_min_date'])})")
        if search == 0:
            print('[-] Nenhum item foi encontrado.')
        print('')
        return 1

    except:
        print(f'[!] Busca inválida\n')
        return 0

while __name__ == '__main__':
    search()
