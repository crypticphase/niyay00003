import tkinter as tk
from tkinter import ttk, messagebox
from nexus.engine.search_engine import SearchEngine

class GlobalSearch(tk.Toplevel):
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.title("Global Search - ค้นหาข้ามโปรเจกต์")
        self.geometry("800x600")
        self.configure(bg="#111", padx=20, pady=20)
        self.engine = engine
        self.search_engine = SearchEngine(engine)
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="🔍 ค้นหาข้ามโปรเจกต์ (Global Search)", bg="#111", fg="#00ff00", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        search_frame = tk.Frame(self, bg="#111")
        search_frame.pack(fill=tk.X, pady=15)
        
        self.search_ent = tk.Entry(search_frame, font=("Segoe UI", 14), bg="#222", fg="white", borderwidth=0, insertbackground="white")
        self.search_ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_ent.focus_set()
        self.search_ent.bind("<Return>", self.do_search)
        
        tk.Button(search_frame, text="ค้นหา", command=self.do_search, bg="#007acc", fg="white", padx=20).pack(side=tk.LEFT)

        # Filters
        filter_frame = tk.Frame(self, bg="#111")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        self.filter_var = tk.StringVar(value="All")
        filters = ["All", "Module", "Story", "Lore", "Fact", "Timeline"]
        for f in filters:
            tk.Radiobutton(filter_frame, text=f, variable=self.filter_var, value=f, bg="#111", fg="#888", selectcolor="#007acc", activebackground="#111", activeforeground="white", command=self.do_search).pack(side=tk.LEFT, padx=5)

        # Results
        self.canvas = tk.Canvas(self, bg="#111", borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.results_frame = tk.Frame(self.canvas, bg="#111")
        
        self.results_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw", width=740)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def do_search(self, evt=None):
        query = self.search_ent.get().strip()
        if not query: return
        
        for w in self.results_frame.winfo_children(): w.destroy()
        
        results = self.search_engine.search(query)
        filter_val = self.filter_var.get()
        
        filtered_results = [r for r in results if filter_val == "All" or r["type"].capitalize() == filter_val]
        
        if not filtered_results:
            tk.Label(self.results_frame, text="ไม่พบผลลัพธ์ที่ตรงกับการค้นหา", bg="#111", fg="#444", font=("Segoe UI", 11)).pack(pady=20)
            return

        for r in filtered_results:
            self.create_result_card(r)

    def create_result_card(self, r):
        card = tk.Frame(self.results_frame, bg="#1a1a1a", pady=10, padx=15)
        card.pack(fill=tk.X, pady=5)
        
        header = tk.Frame(card, bg="#1a1a1a")
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"[{r['category']}]", bg="#1a1a1a", fg="#00ff00", font=("Segoe UI", 8, "bold")).pack(side=tk.LEFT)
        tk.Label(header, text=r["title"], bg="#1a1a1a", fg="white", font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Label(card, text=r["snippet"], bg="#1a1a1a", fg="#888", font=("Segoe UI", 10), justify=tk.LEFT, wraplength=700).pack(fill=tk.X, pady=5)
        
        # Action button
        btn = tk.Button(card, text="เปิดดู →", command=lambda: self.open_result(r), bg="#333", fg="#ccc", relief=tk.FLAT, font=("Segoe UI", 9))
        btn.pack(anchor="e")

    def open_result(self, r):
        # This will depend on the main window's methods
        # For now, we'll just close and tell the user
        messagebox.showinfo("Search", f"กำลังเปิด: {r['title']} ({r['category']})")
        # In a real app, we'd call self.master.show_module_manager(r['data']) etc.
        self.destroy()
