import tkinter as tk
from tkinter import scrolledtext

class LoreWiki(tk.Frame):
    """The Ultimate Searchable Lore Wiki for all world-building entries."""
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="📚 LORE WIKI", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(anchor="w", padx=40, pady=30)
        
        search_frame = tk.Frame(self, bg="#0a0a0a")
        search_frame.pack(fill=tk.X, padx=40)
        tk.Label(search_frame, text="Search Lore:", bg="#0a0a0a", fg="#888").pack(side=tk.LEFT)
        self.search_ent = tk.Entry(search_frame, width=50, bg="#111", fg="white", borderwidth=0)
        self.search_ent.pack(side=tk.LEFT, padx=10)
        
        self.wiki_area = scrolledtext.ScrolledText(self, bg="#0a0a0a", fg="#ccc", font=("Segoe UI", 11), padx=40, borderwidth=0)
        self.wiki_area.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.search_ent.bind("<KeyRelease>", self.do_search)
        self.do_search()

    def do_search(self, evt=None):
        term = self.search_ent.get().lower()
        self.wiki_area.delete("1.0", tk.END)
        for mod, items in self.engine.modules.items():
            for item in items:
                # Search across all fields in item
                match = False
                for val in item.values():
                    if term in str(val).lower():
                        match = True
                        break
                
                if match:
                    self.wiki_area.insert(tk.END, f"[{mod.upper()}] {item.get('name', 'Unnamed')}\n", "header")
                    for k, v in item.items():
                        if k != "name":
                            self.wiki_area.insert(tk.END, f"{k.upper()}: {v}\n")
                    self.wiki_area.insert(tk.END, "\n")
        
        self.wiki_area.tag_config("header", foreground="#00ff00", font=("Segoe UI", 12, "bold"))
