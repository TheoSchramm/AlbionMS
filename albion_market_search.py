import urllib.request, json, tkinter as tk
from tkinter import ttk, messagebox, Toplevel

root = tk.Tk()
root.geometry('280x140')
root.resizable(False, False)
root.title('Market Search')

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
        url = f"https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}{enchantment_func(enchantment)}?locations=LymhurstBridgewatchFortSterlingMartlockThetfordCaerleon&qualities={quality}"
        print(url)
        with urllib.request.urlopen(url) as url_obj:
            data = json.load(url_obj)
    except:
        messagebox.showerror(f'Erro','Item inválido.')
        return 0

    try:
        result = tk.Toplevel(root)
        result.geometry(f"620x200")
        result.resizable(False, False)

        tree = ttk.Treeview(result, columns=('city','sell_price_min','sell_price_min_date'), show='headings')
        tree.heading('city', text='Cidade')
        tree.heading('sell_price_min', text='Preço')
        tree.heading('sell_price_min_date', text='Data')
    
        successful_search = 0
        for i in range(len(data)):
            if data[i]['sell_price_min'] != 0:
                successful_search += 1
                tree.insert('', tk.END, values=(data[i]['city'], f"{data[i]['sell_price_min']:,}", data_func(data[i]['sell_price_min_date'])))
        
        if successful_search == 0:
            result.destroy()
            messagebox.showerror('Erro', 'Nenhum item foi encontrado.')
            return 0

        result.title(f"{successful_search}x {item.title()} (Qualidade: {cbb_quality_value.get()} | Encantamento: {cbb_enchantment_value.get()})")
        result.bind("<Escape>",lambda event: result.destroy())
        result.focus()
        
        tree.grid(row=0, column=0, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(result, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        def copy2clip(event):
            for selected_item in tree.selection():
                key = tree.item(selected_item)
                root.clipboard_clear
                root.clipboard_append("     ".join(key['values']))
                root.update
        tree.bind('<<TreeviewSelect>>', copy2clip)
        
        def tree_sort_column(tree, column, reverse):
            list = [(tree.set(i, column), i) for i in tree.get_children('')]
            list.sort(reverse=reverse)
            for index, (value, i) in enumerate(list):
                tree.move(i, '', index)
            tree.heading(column, command=lambda: \
                tree_sort_column(tree, column, not reverse))
        
        for column,text in zip(('city','sell_price_min','sell_price_min_date'),('Cidade','Preço','Data')):
            tree.heading(column, text=text, command=lambda _column=column: \
                    tree_sort_column(tree, _column, False))
    except:
        result.destroy()
        messagebox.showerror(f'Erro', 'Busca inválida.')
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


b1 = tk.Button(root, height = 1, width = 30, text= 'Procurar...', command = lambda: search(entry_item_name.get(),quality_dict[cbb_quality_value.get()],cbb_enchantment_value.get()))
b1.place(x=25, y=100)

root.bind("<Return>", (lambda event: search(entry_item_name.get(),quality_dict[cbb_quality_value.get()],cbb_enchantment_value.get())))


root.mainloop()
