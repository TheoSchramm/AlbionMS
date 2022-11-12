import urllib.request, json, tkinter as tk
from tkinter import ttk, messagebox, Toplevel

root = tk.Tk()
root.geometry('280x140')
root.resizable(False, False)
root.title("Market Search")

quality_dict = {
    'Qualquer' : 0,
    'Normal' : 1,
    'Bom' : 2,
    'Excepcional' : 3,
    'Excelente' : 4,
    'Obra-prima' : 5,
}

def save_url(index,item,quality,enchantment):
    try:
        with open('fav.json', 'r') as fp:
            data = json.load(fp)
    except:
        with open('fav.json', 'w+') as fp:
            json.dump({}, fp, indent=4)
        save_url(index,item,quality,enchantment)
    else:
        data[index] = item,quality,enchantment
        with open('fav.json', 'w') as fp:
            json.dump(data, fp, indent=4)
        messagebox.showinfo("Item favoritado", f"{item.title()} favoritado na posição F{index}.")
        return 0
    
def open_url(index):
    index = str(index)
    with open('fav.json', 'r') as fp:
        data = json.load(fp)
    search(data[index][0], data[index][1], data[index][2])

def enchantment_func(enchantment_num):
        match enchantment_num:
            case '0':
                return ''
            case _:
                return f'@{enchantment_num}'

def data_func(timestamp):
    return f"{timestamp[8:10]}/{timestamp[5:7]}/{timestamp[0:4]} / {timestamp[11:13]}:{timestamp[14:16]}:{timestamp[17:20]}"


def copy2clip(event, tree):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        root.clipboard_clear()
        root.clipboard_append('   '.join(str(i) for i in record))
        

def tree_sort_column(t, col, reverse):
    l = [(t.set(k, col), k) for k in t.get_children('')]
    try:
        l.sort(key=lambda t: int(t[0].replace(",","")), reverse=reverse)
    except ValueError:
        if col == 'quality':
            l.sort(key=lambda t: quality_dict.__getitem__(t[0]), reverse=reverse)
        else:
            l.sort(reverse=reverse)
            
    for index, (val, k) in enumerate(l):
        t.move(k, '', index)
        t.heading(col, command=lambda _col=col: \
            tree_sort_column(t, _col, not reverse))


def search(item,quality,enchantment):
    try:
        with open('item_list.json' , 'r') as fp:
            item_list = json.load(fp)
        url = f'https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}{enchantment_func(enchantment)}?locations=LymhurstBridgewatchFortSterlingMartlockThetfordCaerleon&qualities={quality}'


    except KeyError:
        messagebox.showerror(f"Erro","Item inválido.")
        return 0
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo JSON não encontrado.")
        return 0

    with urllib.request.urlopen(url) as url_obj:
        data = json.load(url_obj)

    try:
        result = tk.Toplevel(root)
        result.geometry(f"820x245")
        result.resizable(True, False)

        tree = ttk.Treeview(result, columns=('city','sell_price_min','quality','sell_price_min_date'), show='headings')
        tree.heading('city', text="Cidade")
        tree.heading('sell_price_min', text="Preço")
        tree.heading('quality', text="Qualidade")
        tree.heading('sell_price_min_date', text="Data")

        tree.column('city',anchor='center')
        tree.column('sell_price_min',anchor='center')
        tree.column('quality',anchor='center')
        tree.column('sell_price_min_date',anchor='center')

        successful_search = 0
        for i in range(len(data)):
            if data[i]['sell_price_min'] != 0:
                successful_search += 1
                tree.insert('', tk.END, values=(
                    data[i]['city'].replace("Portal",""), 
                    f"{data[i]['sell_price_min']:,}", 
                    list(quality_dict.keys())[list(quality_dict.values()).index(data[i]['quality'])],
                    data_func(data[i]['sell_price_min_date'])))
        
        if not successful_search:
            result.destroy()
            messagebox.showerror("Erro", "Nenhum item foi encontrado.")
            return 0
    
    
        result.title(f"{successful_search}x {item.title()} | Encantamento ({enchantment})")
        tree.grid(row=0, column=0, sticky='nsew')
        result.focus()
        

        scrollbar = ttk.Scrollbar(result, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')


        for col, text in zip(('city','sell_price_min','quality','sell_price_min_date'),("Cidade","Preço","Qualidade","Data")):
            tree.heading(col, text=text, command=lambda _col=col: \
                tree_sort_column(tree, _col, False))
                

        tree.bind('<<TreeviewSelect>>', lambda event: copy2clip(None, tree))
        result.bind('<Escape>',lambda event: result.destroy())
        result.bind('<F1>', (lambda event: save_url(1,item,quality,int(enchantment))))
        result.bind('<F2>', (lambda event: save_url(2,item,quality,int(enchantment))))
        result.bind('<F3>', (lambda event: save_url(3,item,quality,int(enchantment))))
        result.bind('<F4>', (lambda event: save_url(4,item,quality,int(enchantment))))
        result.bind('<F5>', (lambda event: save_url(5,item,quality,int(enchantment))))
        result.bind('<F6>', (lambda event: save_url(6,item,quality,int(enchantment))))
        result.bind('<F7>', (lambda event: save_url(7,item,quality,int(enchantment))))
        result.bind('<F8>', (lambda event: save_url(8,item,quality,int(enchantment))))
        result.bind('<F9>', (lambda event: save_url(9,item,quality,int(enchantment))))
        result.bind('<F10>', (lambda event: save_url(10,item,quality,int(enchantment))))
        result.bind('<F11>', (lambda event: save_url(11,item,quality,int(enchantment))))
        result.bind('<F12>', (lambda event: save_url(12,item,quality,int(enchantment))))


    except:
        result.destroy()
        messagebox.showerror(f"Erro", "Busca inválida.")
        return 0


lbl_item_name = tk.Label(text = "Nome do item:")
lbl_item_name.place(x=10, y=10)


lbl_quality = tk.Label(text = "Qualidade:")
lbl_quality.place(x=20, y=40)


lbl_enchantment = tk.Label(text = "Encantamento:")
lbl_enchantment.place(x=10, y=70)


entry_item_name = tk.Entry(root)
entry_item_name.place(x=100, y=10, height = 20, width = 150)


cbb_quality_value = tk.StringVar()
cbb_quality = ttk.Combobox(root, textvariable = cbb_quality_value, width=11)
cbb_quality['values'] = ["Qualquer","Normal","Bom","Excepcional","Excelente","Obra-prima"]
cbb_quality['state'] = 'readonly'
cbb_quality.current(0)
cbb_quality.place(x=100, y=40)


cbb_enchantment_value = tk.StringVar()
cbb_enchantment = ttk.Combobox(root, textvariable = cbb_enchantment_value, width = 2)
cbb_enchantment['values'] = [0,1,2,3]
cbb_enchantment['state'] = 'readonly'
cbb_enchantment.current(0)
cbb_enchantment.place(x=100, y=70)


b1 = tk.Button(root, height = 1, width = 30, text= "Procurar...", command = lambda: search(entry_item_name.get().lower(),quality_dict[cbb_quality_value.get()],cbb_enchantment_value.get()))
b1.place(x=25, y=100)


root.bind("<Return>", (lambda event: search(entry_item_name.get().lower(),quality_dict[cbb_quality_value.get()],cbb_enchantment_value.get())))
root.bind("<F1>",(lambda event: open_url(1)))
root.bind("<F2>",(lambda event: open_url(2)))
root.bind("<F3>",(lambda event: open_url(3)))
root.bind("<F4>",(lambda event: open_url(4)))
root.bind("<F5>",(lambda event: open_url(5)))
root.bind("<F6>",(lambda event: open_url(6)))
root.bind("<F7>",(lambda event: open_url(7)))
root.bind("<F8>",(lambda event: open_url(8)))
root.bind("<F9>",(lambda event: open_url(9)))
root.bind("<F10>",(lambda event: open_url(10)))
root.bind("<F11>",(lambda event: open_url(11)))
root.bind("<F12>",(lambda event: open_url(12)))


root.mainloop()
