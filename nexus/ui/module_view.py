import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ModuleManager(tk.Frame):
    """The Ultimate Dynamic Module Manager with Custom Schema, Tags, and Relationships."""
    def __init__(self, parent, engine, ai, mod_name):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.ai = ai
        self.mod_name = mod_name
        self.data = self.engine.modules.get(mod_name, [])
        self.schema = self.engine.config.get("schemas", {}).get(mod_name, ["name", "details"])
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0a0a0a")
        header.pack(fill=tk.X, padx=40, pady=30)
        tk.Label(header, text=f"📦 {self.mod_name.replace('_', ' ').upper()}", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        btn_row = tk.Frame(header, bg="#0a0a0a")
        btn_row.pack(side=tk.RIGHT)
        
        tk.Button(btn_row, text="✨ AI สร้างข้อมูล", command=self.ai_gen, bg="#8a2be2", fg="white", font=("Segoe UI", 9, "bold"), padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="⚙️ ตั้งค่าฟิลด์", command=self.edit_schema, bg="#333", fg="white", font=("Segoe UI", 9, "bold"), padx=10).pack(side=tk.LEFT, padx=5)

        list_frame = tk.Frame(self, bg="#0a0a0a")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Left Listbox
        self.lb = tk.Listbox(list_frame, width=35, height=25, bg="#111", fg="#ccc", font=("Segoe UI", 11), borderwidth=0, selectbackground="#007acc")
        self.lb.pack(side=tk.LEFT, fill=tk.Y)
        
        for item in self.data: self.lb.insert(tk.END, item.get("name", "Unnamed"))
        
        # Right Editor
        self.edit_scroll = tk.Canvas(list_frame, bg="#0a0a0a", highlightthickness=0)
        self.edit_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30)
        
        self.edit_frame = tk.Frame(self.edit_scroll, bg="#0a0a0a")
        self.edit_scroll.create_window((0,0), window=self.edit_frame, anchor="nw")
        
        self.fields_widgets = {}
        self.render_fields()
        
        self.lb.bind('<<ListboxSelect>>', self.on_select)
        
        # Action Buttons
        btn_row = tk.Frame(self.edit_frame, bg="#0a0a0a")
        btn_row.pack(pady=30, anchor="w")
        tk.Button(btn_row, text="อัปเดตข้อมูล", command=self.save_item, bg="#007acc", fg="white", width=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="เพิ่มใหม่", command=self.add_new, bg="#222", fg="white", width=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="ลบข้อมูล", command=self.delete_item, bg="#cc0000", fg="white", width=10, pady=8).pack(side=tk.LEFT, padx=20)

    def render_fields(self):
        for widget in self.edit_frame.winfo_children():
            if not isinstance(widget, tk.Frame): widget.destroy()
            
        self.fields_widgets = {}
        
        # Dynamic Fields from Schema
        for field in self.schema:
            tk.Label(self.edit_frame, text=field.upper(), bg="#0a0a0a", fg="#444", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10,0))
            if field in ["details", "backstory", "description", "personality", "abilities"]:
                txt = tk.Text(self.edit_frame, width=70, height=8, bg="#111", fg="white", font=("Segoe UI", 11), borderwidth=0, insertbackground="white")
                txt.pack(pady=5, anchor="w")
                self.fields_widgets[field] = txt
            else:
                ent = tk.Entry(self.edit_frame, width=50, font=("Segoe UI", 12), bg="#111", fg="white", borderwidth=0, insertbackground="white")
                ent.pack(pady=5, anchor="w")
                self.fields_widgets[field] = ent

        # Standard Fields: Tags & Relationships
        tk.Label(self.edit_frame, text="แท็ก (คั่นด้วยคอมม่า)", bg="#0a0a0a", fg="#444", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(15,0))
        self.tags_ent = tk.Entry(self.edit_frame, width=50, font=("Segoe UI", 12), bg="#111", fg="#ccc", borderwidth=0)
        self.tags_ent.pack(pady=5, anchor="w")
        
        tk.Label(self.edit_frame, text="ความสัมพันธ์ (เชื่อมโยงข้อมูล)", bg="#0a0a0a", fg="#444", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(15,0))
        self.rel_ent = tk.Entry(self.edit_frame, width=50, font=("Segoe UI", 12), bg="#111", fg="#ccc", borderwidth=0)
        self.rel_ent.pack(pady=5, anchor="w")

    def edit_schema(self):
        win = tk.Toplevel(self)
        win.title(f"Schema Editor: {self.mod_name}")
        win.geometry("400x400")
        win.configure(bg="#1a1a1a", padx=20, pady=20)
        
        tk.Label(win, text="Fields (comma separated):", bg="#1a1a1a", fg="white").pack(pady=10)
        ent = tk.Entry(win, width=50)
        ent.insert(0, ", ".join(self.schema))
        ent.pack(pady=10)
        
        def save():
            new_schema = [f.strip() for f in ent.get().split(",") if f.strip()]
            self.engine.config["schemas"][self.mod_name] = new_schema
            self.schema = new_schema
            self.render_fields()
            self.engine.save()
            win.destroy()
            
        tk.Button(win, text="Save Schema", command=save, bg="#007acc", fg="white").pack(pady=20)

    def ai_gen(self):
        ctx = f"World: {self.engine.world['world_name']}\nGenre: {self.engine.config['genre']}\nLore: {self.engine.world['history_summary']}"
        res = self.ai.generate_lore(self.mod_name, self.schema, ctx)
        
        new_item = {f: "" for f in self.schema}
        new_item["name"] = f"AI {self.mod_name.capitalize()}"
        new_item["details"] = res
        new_item["tags"] = ""
        new_item["relations"] = ""
        
        self.data.append(new_item)
        self.lb.insert(tk.END, new_item["name"])
        self.lb.selection_clear(0, tk.END)
        self.lb.selection_set(tk.END)
        self.on_select(None)

    def on_select(self, evt):
        if self.lb.curselection():
            idx = self.lb.curselection()[0]
            item = self.data[idx]
            for field, widget in self.fields_widgets.items():
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", item.get(field, ""))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, item.get(field, ""))
            
            self.tags_ent.delete(0, tk.END)
            self.tags_ent.insert(0, item.get("tags", ""))
            self.rel_ent.delete(0, tk.END)
            self.rel_ent.insert(0, item.get("relations", ""))

    def save_item(self):
        if self.lb.curselection():
            idx = self.lb.curselection()[0]
            for field, widget in self.fields_widgets.items():
                if isinstance(widget, tk.Text):
                    self.data[idx][field] = widget.get("1.0", tk.END).strip()
                else:
                    self.data[idx][field] = widget.get()
            
            self.data[idx]["tags"] = self.tags_ent.get()
            self.data[idx]["relations"] = self.rel_ent.get()
            
            self.lb.delete(idx)
            self.lb.insert(idx, self.data[idx].get("name", "Unnamed"))
            self.engine.save()
            messagebox.showinfo("Nexus", "Entry updated.")

    def add_new(self):
        new_item = {f: "" for f in self.schema}
        new_item["name"] = "New Entry"
        new_item["tags"] = ""
        new_item["relations"] = ""
        self.data.append(new_item)
        self.lb.insert(tk.END, "New Entry")

    def delete_item(self):
        if self.lb.curselection():
            idx = self.lb.curselection()[0]
            self.data.pop(idx)
            self.lb.delete(idx)
            self.engine.save()
