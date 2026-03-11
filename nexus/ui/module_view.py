import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ModuleManager(tk.Frame):
    """Dynamic Module Manager for characters, items, etc."""
    def __init__(self, parent, engine, ai, mod_name):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.ai = ai
        self.mod_name = mod_name
        self.data = self.engine.modules.get(mod_name, [])
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0a0a0a")
        header.pack(fill=tk.X, padx=40, pady=30)
        tk.Label(header, text=f"📦 {self.mod_name.replace('_', ' ').upper()}", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        tk.Button(header, text="✨ AI GENERATE", command=self.ai_gen, bg="#8a2be2", fg="white", font=("Segoe UI", 9, "bold"), padx=15).pack(side=tk.RIGHT)

        list_frame = tk.Frame(self, bg="#0a0a0a")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        self.lb = tk.Listbox(list_frame, width=35, height=25, bg="#111", fg="#ccc", font=("Segoe UI", 11), borderwidth=0)
        self.lb.pack(side=tk.LEFT, fill=tk.Y)
        
        for item in self.data: self.lb.insert(tk.END, item.get("name", "Unnamed"))
        
        self.edit_frame = tk.Frame(list_frame, bg="#0a0a0a", padx=30)
        self.edit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(self.edit_frame, text="NAME", bg="#0a0a0a", fg="#444", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.name_ent = tk.Entry(self.edit_frame, width=50, font=("Segoe UI", 14), bg="#111", fg="white", borderwidth=0)
        self.name_ent.pack(pady=5, anchor="w")
        
        tk.Label(self.edit_frame, text="DETAILS", bg="#0a0a0a", fg="#444", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(20,0))
        self.desc_text = tk.Text(self.edit_frame, width=70, height=20, bg="#111", fg="white", font=("Segoe UI", 11), borderwidth=0)
        self.desc_text.pack(pady=5, anchor="w")
        
        self.lb.bind('<<ListboxSelect>>', self.on_select)
        
        btn_row = tk.Frame(self.edit_frame, bg="#0a0a0a")
        btn_row.pack(pady=30, anchor="w")
        tk.Button(btn_row, text="UPDATE", command=self.save_item, bg="#007acc", fg="white", width=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="ADD NEW", command=self.add_new, bg="#222", fg="white", width=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="DELETE", command=self.delete_item, bg="#cc0000", fg="white", width=10, pady=8).pack(side=tk.LEFT, padx=20)

    def ai_gen(self):
        ctx = f"World: {self.engine.world['world_name']}\nGenre: {self.engine.config['genre']}\nLore: {self.engine.world['history_summary']}"
        res = self.ai.generate_lore(self.mod_name, ctx)
        lines = res.split("\n")
        name, details = "AI Generated", res
        for l in lines:
            if l.startswith("Name:"): name = l.replace("Name:", "").strip()
            if l.startswith("Details:"): details = l.replace("Details:", "").strip()
        
        self.data.append({"name": name, "details": details})
        self.lb.insert(tk.END, name)
        self.lb.selection_clear(0, tk.END)
        self.lb.selection_set(tk.END)
        self.on_select(None)

    def on_select(self, evt):
        if self.lb.curselection():
            idx = self.lb.curselection()[0]
            item = self.data[idx]
            self.name_ent.delete(0, tk.END)
            self.name_ent.insert(0, item.get("name", ""))
            self.desc_text.delete("1.0", tk.END)
            self.desc_text.insert("1.0", item.get("details", ""))

    def save_item(self):
        if self.lb.curselection():
            idx = self.lb.curselection()[0]
            self.data[idx]["name"] = self.name_ent.get()
            self.data[idx]["details"] = self.desc_text.get("1.0", tk.END).strip()
            self.lb.delete(idx)
            self.lb.insert(idx, self.name_ent.get())
            self.engine.save()
            messagebox.showinfo("Nexus", "Entry updated.")

    def add_new(self):
        self.data.append({"name": "New Entry", "details": ""})
        self.lb.insert(tk.END, "New Entry")

    def delete_item(self):
        if self.lb.curselection():
            idx = self.lb.curselection()[0]
            self.data.pop(idx)
            self.lb.delete(idx)
            self.engine.save()
