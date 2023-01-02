import urllib.request, json, tkinter as tk
from tkinter import ttk, messagebox, Toplevel

quality_dict = {
    'Qualquer' : 0,
    'Normal' : 1,
    'Bom' : 2,
    'Excepcional' : 3,
    'Excelente' : 4,
    'Obra-prima' : 5,
}

class MenuWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('280x140')
        self.resizable(False, False)
        self.title("Market Search")
        
        self.lbl_item_name = tk.Label(self, text = "Nome do item:")
        self.lbl_item_name.place(x=10, y=10)

        self.lbl_quality = tk.Label(self, text = "Qualidade:")
        self.lbl_quality.place(x=20, y=40)

        self.lbl_enchantment = tk.Label(self, text = "Encantamento:")
        self.lbl_enchantment.place(x=10, y=70)

        self.entry_item_name = tk.Entry(self)
        self.entry_item_name.place(x=100, y=10, height = 20, width = 150)

        self.cbb_quality = ttk.Combobox(self, width=11)
        self.cbb_quality['values'] = list(quality_dict.keys())
        self.cbb_quality['state'] = 'readonly'
        self.cbb_quality.current(0)
        self.cbb_quality.place(x=100, y=40)

        self.cbb_enchantment = ttk.Combobox(self, width = 2)
        self.cbb_enchantment['values'] = [i for i in range(5)]
        self.cbb_enchantment['state'] = 'readonly'
        self.cbb_enchantment.current(0)
        self.cbb_enchantment.place(x=100, y=70)

        self.b1 = tk.Button(self, height = 1, width = 30, text= "Procurar...", command = lambda: self.start_search(self))
        self.b1.place(x=25, y=100)

        for i in range(1,13):
            self.bind(f"<F{i}>", lambda event, i=i: self.open_url(self, i))
        self.bind("<Return>", lambda event: self.start_search(self))

    def enchantment_func(self, root, enchantment_num):
            match enchantment_num:
                case 0:
                    return ''
                case _:
                    return f'@{enchantment_num}'

    def open_url(self, root, index):
        index = str(index)
        with open('fav.json', 'r') as fp:
            data = json.load(fp)
        self.search(self, data[index][0], data[index][1], data[index][2])

    def start_search(self, root):
        self.search(self,self.entry_item_name.get().lower(),quality_dict[self.cbb_quality.get()],int(self.cbb_enchantment.get()))

    def search(self,root,item,quality,enchantment):
        try:
            with urllib.request.urlopen("https://github.com/TheoSchramm/albion/raw/main/item_list.json") as url_obj:
                item_list = json.load(url_obj)
            url = f'https://www.albion-online-data.com/api/v2/stats/prices/{item_list[item]}{self.enchantment_func(self, enchantment)}?locations=LymhurstBridgewatchFortSterlingMartlockThetfordCaerleon&qualities={quality}'
        except KeyError:
            messagebox.showerror(f"Erro","Item inválido.")
            return None
        except urllib.error.HTTPError:
            messagebox.showerror("Erro", "Sem conexão com a internet.")
            return None
        with urllib.request.urlopen(url) as url_obj:
            data = json.load(url_obj)
        ResultWin(self, data, item, quality, enchantment)

class ResultWin(Toplevel):        
        def __init__(self, root, data, item, quality, enchantment):
            super().__init__(root)
            self.geometry(f"820x245")
            self.resizable(True, False)
            self.focus()

            self.colunas_dic = {
                'city' : 'Cidade',
                'sell_price_min' : 'Preço',
                'quality' : 'Qualidade',
                'sell_price_min_date' : 'Data'
            }

            self.tree = ttk.Treeview(self, columns=list(self.colunas_dic.keys()), show='headings')
            self.tree.grid(row=0, column=0, sticky='nsew')
            
            self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree.configure(yscroll=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky='ns')
            
            for i in self.colunas_dic:
                self.tree.heading(i, text= self.colunas_dic[i], anchor='center')
                self.tree.column(i, anchor='center')
            
            self.successful_search = 0
            try:
                for i in range(len(data)):
                    if data[i]['sell_price_min'] != 0:
                        self.successful_search += 1
                        self.tree.insert('', tk.END, values=(
                            data[i]['city'].replace("Portal",""), 
                            f"{data[i]['sell_price_min']:,}", 
                            list(quality_dict.keys())[list(quality_dict.values()).index(data[i]['quality'])],
                            self.data_func(self,data[i]['sell_price_min_date'])))
                if not self.successful_search:
                    self.destroy()
                    messagebox.showerror("Erro", "Nenhum item foi encontrado.")
                    return None
                self.title(f"{self.successful_search}x {item.title()} | Encantamento ({enchantment})")

                for col, text in self.colunas_dic.items():
                    self.tree.heading(col, text=text, command=lambda _col=col: \
                        self.tree_sort_column(self, self.tree, _col, False))

                for i in range(1,13):
                    self.bind(f'<F{i}>', lambda event, i=i: self.save_url(self, i, item, quality, enchantment))
                self.bind('<Escape>', lambda event: self.destroy())
                self.tree.bind('<<TreeviewSelect>>', lambda event: self.copy2clip(self, None, self.tree))

            except:
                self.destroy()
                messagebox.showerror(f"Erro", "Busca inválida.")
                return None
            
        def data_func(self, root, timestamp):
            return f"{timestamp[8:10]}/{timestamp[5:7]}/{timestamp[0:4]} / {timestamp[11:13]}:{timestamp[14:16]}:{timestamp[17:20]}"

        def copy2clip(self, root, event, tree):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                self.clipboard_clear()
                self.clipboard_append('   '.join(str(i) for i in record))
        
        def tree_sort_column(self, root, t, col, reverse):
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
                    self.tree_sort_column(self, t, _col, not reverse))
        
        def save_url(self, root, index, item, quality, enchantment):
            try:
                with open('fav.json', 'r') as fp:
                    data = json.load(fp)
            except:
                with open('fav.json', 'w+') as fp:
                    json.dump({}, fp, indent=4)
                self.save_url(index,item,quality,enchantment)
            else:
                data[index] = item,quality,enchantment
                with open('fav.json', 'w') as fp:
                    json.dump(data, fp, indent=4)
                messagebox.showinfo("Item favoritado", f"{item.title()} favoritado na posição F{index}.")
                self.focus()

if __name__ == "__main__":
    MenuWin().mainloop()
