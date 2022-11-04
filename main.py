import urllib.request, json

cities ='''
Lymhurst,
Bridgewatch,
FortSterling,
Martlock,
Thetford,
Caerleon'''.replace('\n','')

quality_dict = {
    '0': 'All',
    '1': 'Normal',
    '2': 'Good',
    '3': 'Outstanding',
    '4': 'Excellent',
    '5': 'Masterpiece',
}

def search(item,quality):
    try:
        with open('item_list.json' , 'r') as fp:
            item_list = json.load(fp)
    except:
        print('[-] Arquivo JSON não encontrado!\n')
        return 0
    
    try:
        with urllib.request.urlopen(f"https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}?locations={cities}&qualities={quality}") as url:
            data = json.load(url)
    except:
        print(f'[-] Erro! {item.title()} não existe!\n')
        return 0
    
    def quality_func(quality_num):
        match quality_num:
            case '0':
                return f" Qualidade: {quality_dict[str(data[i]['quality'])]}"
            case _:
                return ''
    
    def data_func(timestamp):
        return f'{timestamp[8:10]}/{timestamp[5:7]}/{timestamp[0:4]} / {timestamp[11:13]}:{timestamp[14:16]}:{timestamp[17:20]}'

    try:
        print(f"\n[+] Procurando por: {item.title()} | Qualidade: {quality_dict[quality]}")
        for i in range(len(data)):
            try:
                if data[i]['sell_price_min'] != 0:
                    print(f"[=] {data[i]['city']}: ${data[i]['sell_price_min']:,} |{quality_func(quality)} ({data_func(data[i]['sell_price_min_date'])})")
            except:
                pass
        print('')
    except:
        print(f'[-] Erro! Qualidade inválida\n')
        return 0

while __name__ == '__main__':
    search(input('[+] Digite o nome do item para buscar: '),input('[+] Digite o número da qualidade desejada (0/1/2/3/4/5): '))
