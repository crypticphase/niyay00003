import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class PlotPlanner(tk.Frame):
    """The Ultimate Plot Planner with Three-Act Structure and Scene Graph."""
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0a0a0a")
        header.pack(fill=tk.X, padx=40, pady=30)
        tk.Label(header, text="🗺️ PLOT PLANNER", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        main_frame = tk.Frame(self, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Treeview for Plot
        self.tree = ttk.Treeview(main_frame, columns=("Summary", "Status"), height=25)
        self.tree.heading("#0", text="Act / Scene")
        self.tree.heading("Summary", text="Summary")
        self.tree.heading("Status", text="Status")
        self.tree.column("#0", width=250)
        self.tree.column("Summary", width=500)
        self.tree.column("Status", width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.refresh_tree()
        
        ctrl_frame = tk.Frame(main_frame, bg="#0a0a0a", padx=20)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Button(ctrl_frame, text="ADD ACT", command=self.add_act, width=20, pady=10).pack(pady=5)
        tk.Button(ctrl_frame, text="ADD SCENE", command=self.add_scene, width=20, pady=10).pack(pady=5)
        tk.Button(ctrl_frame, text="EDIT SELECTED", command=self.edit_selected, width=20, pady=10).pack(pady=5)
        tk.Button(ctrl_frame, text="SAVE PLOT", command=self.engine.save, bg="#007acc", fg="white", width=20, pady=10).pack(pady=20)

    def refresh_tree(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, act in enumerate(self.engine.plot["acts"]):
            act_id = self.tree.insert("", tk.END, text=act["title"], open=True, tags=("act",))
            for j, scene in enumerate(act.get("scenes", [])):
                self.tree.insert(act_id, tk.END, text=scene["title"], values=(scene.get("summary", ""), scene.get("status", "Draft")), tags=("scene",))
        
        self.tree.tag_configure("act", font=("Segoe UI", 11, "bold"), foreground="#00ff00")

    def add_act(self):
        self.engine.plot["acts"].append({"title": "New Act", "scenes": []})
        self.refresh_tree()

    def add_scene(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Nexus", "Select an Act first.")
        
        item = self.tree.item(sel[0])
        act_title = item['text']
        
        for act in self.engine.plot["acts"]:
            if act["title"] == act_title:
                act["scenes"].append({"title": "New Scene", "summary": "", "status": "Draft"})
                break
        self.refresh_tree()

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel: return
        
        item = self.tree.item(sel[0])
        title = item['text']
        
        win = tk.Toplevel(self)
        win.title(f"Edit: {title}")
        win.geometry("400x400")
        
        tk.Label(win, text="Title:").pack(pady=10)
        ent = tk.Entry(win, width=40)
        ent.insert(0, title)
        ent.pack()
        
        tk.Label(win, text="Summary:").pack(pady=10)
        txt = scrolledtext.ScrolledText(win, width=40, height=10)
        txt.insert("1.0", item['values'][0] if item['values'] else "")
        txt.pack()
        
        def save():
            new_title = ent.get()
            new_summary = txt.get("1.0", tk.END).strip()
            
            # Update in engine
            for act in self.engine.plot["acts"]:
                if act["title"] == title:
                    act["title"] = new_title
                    break
                for scene in act["scenes"]:
                    if scene["title"] == title:
                        scene["title"] = new_title
                        scene["summary"] = new_summary
                        break
            
            self.refresh_tree()
            win.destroy()
            
        tk.Button(win, text="Save", command=save).pack(pady=20)
