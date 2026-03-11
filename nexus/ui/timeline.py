import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class TimelineView(tk.Frame):
    """The Ultimate History Timeline with Eras and Events."""
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0a0a0a")
        header.pack(fill=tk.X, padx=40, pady=30)
        tk.Label(header, text="📜 WORLD TIMELINE", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        main_frame = tk.Frame(self, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Treeview for Timeline
        self.tree = ttk.Treeview(main_frame, columns=("Year", "Description"), height=25)
        self.tree.heading("#0", text="Era / Event")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Description", text="Description")
        self.tree.column("#0", width=250)
        self.tree.column("Year", width=100)
        self.tree.column("Description", width=500)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.refresh_tree()
        
        ctrl_frame = tk.Frame(main_frame, bg="#0a0a0a", padx=20)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Button(ctrl_frame, text="ADD ERA", command=self.add_era, width=20, pady=10).pack(pady=5)
        tk.Button(ctrl_frame, text="ADD EVENT", command=self.add_event, width=20, pady=10).pack(pady=5)
        tk.Button(ctrl_frame, text="SAVE TIMELINE", command=self.engine.save, bg="#007acc", fg="white", width=20, pady=10).pack(pady=20)

    def refresh_tree(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, era in enumerate(self.engine.timeline["eras"]):
            era_id = self.tree.insert("", tk.END, text=era["name"], open=True, tags=("era",))
            for j, event in enumerate(era.get("events", [])):
                self.tree.insert(era_id, tk.END, text=event["name"], values=(event.get("year", ""), event.get("description", "")), tags=("event",))
        
        self.tree.tag_configure("era", font=("Segoe UI", 11, "bold"), foreground="#00ff00")

    def add_era(self):
        self.engine.timeline["eras"].append({"name": "New Era", "events": []})
        self.refresh_tree()

    def add_event(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Nexus", "Select an Era first.")
        
        item = self.tree.item(sel[0])
        era_name = item['text']
        
        for era in self.engine.timeline["eras"]:
            if era["name"] == era_name:
                era["events"].append({"name": "New Event", "year": "1000", "description": ""})
                break
        self.refresh_tree()
