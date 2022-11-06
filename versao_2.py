import urllib.request, json, tkinter as tk
from tkinter import ttk, messagebox, Toplevel

root = tk.Tk()
root.geometry('280x140')
root.resizable(False, False)
root.title('Albion Market Search')

quality_dict = {
    'Qualquer' : 0,
    'Normal' : 1,
    'Bom' : 2,
    'Excepcional' : 3,
    'Excelente' : 4,
    'Obra-prima' : 5,
}

def enchantment_func(enchantment_num):
        match enchantment_num:
            case '0':
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
        messagebox.showerror('Erro', 'Arquivo JSON não encontrado.')
        return 0

    try:
        url = f"https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}{enchantment_func(enchantment)}?locations=LymhurstBridgewatchFortSterlingMartlock,ThetfordCaerleon&qualities=qualities={quality}"
        with urllib.request.urlopen(url) as url_obj:
            data = json.load(url_obj)
    except:
        messagebox.showerror(f'Erro','Item inválido.')
        return 0

    try:
        result = tk.Toplevel(root)
        result.resizable(False, False)
        result_dynamic_height = 20
        result.geometry(f"400x{result_dynamic_height}")
        txt_dynamic_height = 0
        result_search = 0
        tk.Label(result, text = f"Qualidade: {cbb_quality_value.get()} | Encantamento: {cbb_enchantment_value.get()}").place(x=0, y=txt_dynamic_height)
        for i in range(len(data)):
            if data[i]['sell_price_min'] != 0:
                result_search += 1
                result_dynamic_height += 20
                txt_dynamic_height += 20
                tk.Label(result,text = f"({result_search}) {data[i]['city']}: ${data[i]['sell_price_min']:,} ({data_func(data[i]['sell_price_min_date'])})\n").place(x=0, y=txt_dynamic_height)

        if result_search == 0:
            result.destroy()
            messagebox.showerror('Erro', 'Nenhum item foi encontrado.')
            return 0

        result.geometry(f"400x{result_dynamic_height}")
        result.title(f"{result_search}x {item.title()}")
    except:
        messagebox.showerror(f'Erro', 'Busca inválida.')
        return 0


lbl_item_name = ttk.Label(text = "Nome do item:")
lbl_item_name.place(x=10, y=10)

lbl_quality = ttk.Label(text = "Qualidade:")
lbl_quality.place(x=20, y=40)

lbl_enchantment = ttk.Label(text = "Encantamento:")
lbl_enchantment.place(x=10, y=70)


entry_item_name = tk.Entry(root)
entry_item_name.place(x=100, y=10, height = 20, width = 150)


cbb_quality_value = tk.StringVar()
cbb_quality = ttk.Combobox(root, textvariable = cbb_quality_value, width=11)
cbb_quality['values'] = ['Qualquer','Normal','Bom','Excepcional','Excelente','Obra-prima']
cbb_quality['state'] = 'readonly'
cbb_quality.current(0)
cbb_quality.place(x=100, y=40)


cbb_enchantment_value = tk.StringVar()
cbb_enchantment = ttk.Combobox(root, textvariable = cbb_enchantment_value, width = 2)
cbb_enchantment['values'] = [0,1,2,3]
cbb_enchantment['state'] = 'readonly'
cbb_enchantment.current(0)
cbb_enchantment.place(x=100, y=70)


b1 = tk.Button(root, height = 1, width = 30, text= 'Pesquisar', command = lambda: search(entry_item_name.get(),quality_dict[cbb_quality_value.get()],cbb_enchantment_value.get()))
b1.place(x=25, y=100)
root.mainloop()
