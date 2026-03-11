import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from nexus.engine.project_manager import ProjectManager
from nexus.engine.ai_connector import AIConnector
from nexus.ui.editor import StoryEditor
from nexus.ui.module_view import ModuleManager
from nexus.ui.ai_panel import AIPanel
from nexus.ui.wiki import LoreWiki
import os

class MainWindow(tk.Tk):
    """Main Application Window for Nexus God Writer."""
    def __init__(self):
        super().__init__()
        self.title("NEXUS GOD WRITER - Advanced Worldbuilding & Story Engine")
        self.geometry("1400x900")
        self.configure(bg="#0a0a0a")
        
        self.engine = ProjectManager()
        self.ai = AIConnector()
        
        self.setup_layout()
        self.show_welcome()

    def setup_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, width=250, bg="#111", padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(self.sidebar, text="NEXUS", font=("Impact", 28), bg="#111", fg="#00ff00").pack(pady=20)
        
        self.nav_frame = tk.Frame(self.sidebar, bg="#111")
        self.nav_frame.pack(fill=tk.BOTH, expand=True)

        # Main Content
        self.content = tk.Frame(self, bg="#0a0a0a")
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_sidebar(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
            
        nav_items = [
            ("🌍 World Wizard", self.show_world_config),
            ("📖 Story Editor", self.show_editor),
            ("📚 Lore Wiki", self.show_lore_wiki),
            ("🤖 AI Assistant", self.show_ai_panel),
        ]
        
        if self.engine.current_id:
            tk.Label(self.nav_frame, text="MODULES", font=("Segoe UI", 8, "bold"), bg="#111", fg="#444").pack(pady=(15, 5), anchor="w", padx=10)
            for mod in self.engine.config.get("modules", []):
                label = f"  {mod.replace('_', ' ').capitalize()}"
                nav_items.append((label, lambda m=mod: self.show_module_manager(m)))

        nav_items.append(("", None)) # Spacer
        nav_items.append(("📤 Export Project", self.export_project))
        nav_items.append(("🏠 Home", self.show_welcome))

        for text, cmd in nav_items:
            if not text:
                tk.Frame(self.nav_frame, height=1, bg="#222").pack(fill=tk.X, pady=10)
                continue
            btn = tk.Button(self.nav_frame, text=text, command=cmd, bg="#111", fg="#ccc", 
                            relief=tk.FLAT, anchor="w", padx=15, pady=8, font=("Segoe UI", 10),
                            activebackground="#222", activeforeground="white")
            btn.pack(fill=tk.X)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_content()
        self.update_sidebar()
        
        frame = tk.Frame(self.content, bg="#0a0a0a")
        frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        tk.Label(frame, text="NEXUS GOD WRITER", font=("Impact", 56), bg="#0a0a0a", fg="white").pack()
        tk.Label(frame, text="The Ultimate Worldbuilding & Story Engine", font=("Segoe UI", 16), bg="#0a0a0a", fg="#666").pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg="#0a0a0a")
        btn_frame.pack(pady=40)
        
        tk.Button(btn_frame, text="CREATE NEW WORLD", command=self.dialog_new_project, width=25, bg="#007acc", fg="white", pady=12, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="LOAD EXISTING", command=self.dialog_load_project, width=25, bg="#222", fg="white", pady=12, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)

    def dialog_new_project(self):
        win = tk.Toplevel(self)
        win.title("Initialize New Nexus")
        win.geometry("450x500")
        win.configure(padx=30, pady=30, bg="#1a1a1a")
        
        tk.Label(win, text="Project Name", bg="#1a1a1a", fg="#888").pack(anchor="w")
        name_ent = tk.Entry(win, width=40, font=("Segoe UI", 11), bg="#222", fg="white")
        name_ent.pack(pady=5)
        
        tk.Label(win, text="Genre", bg="#1a1a1a", fg="#888").pack(anchor="w", pady=(10,0))
        genre_ent = tk.Entry(win, width=40, font=("Segoe UI", 11), bg="#222", fg="white")
        genre_ent.pack(pady=5)
        
        tk.Label(win, text="World Type", bg="#1a1a1a", fg="#888").pack(anchor="w", pady=(10,0))
        wtype_var = tk.StringVar(value="fantasy")
        cb = ttk.Combobox(win, textvariable=wtype_var, values=["fantasy", "sci-fi", "cyberpunk", "horror", "romance", "historical"])
        cb.pack(pady=5, fill=tk.X)
        
        def create():
            if name_ent.get():
                self.engine.create(name_ent.get(), genre_ent.get(), wtype_var.get())
                win.destroy()
                self.show_world_config()
            else:
                messagebox.showwarning("Nexus", "Project name is mandatory.")
                
        tk.Button(win, text="GENERATE PROJECT", command=create, bg="#00ff00", fg="black", pady=12, font=("Segoe UI", 11, "bold")).pack(pady=30, fill=tk.X)

    def dialog_load_project(self):
        projects = [d for d in os.listdir("projects") if os.path.isdir(os.path.join("projects", d))]
        if not projects: return messagebox.showinfo("Nexus", "No projects found.")
        
        win = tk.Toplevel(self)
        win.title("Select Project")
        win.geometry("400x500")
        win.configure(bg="#1a1a1a", padx=20, pady=20)
        
        lb = tk.Listbox(win, width=50, height=18, bg="#111", fg="#ccc", font=("Segoe UI", 10))
        lb.pack(pady=10)
        for p in projects: lb.insert(tk.END, p)
        
        def load():
            if lb.curselection():
                self.engine.load(lb.get(lb.curselection()))
                win.destroy()
                self.show_world_config()
        
        tk.Button(win, text="OPEN PROJECT", command=load, bg="#007acc", fg="white", pady=10).pack(fill=tk.X)

    def show_world_config(self):
        self.clear_content()
        self.update_sidebar()
        tk.Label(self.content, text="🌍 WORLD WIZARD", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(anchor="w", padx=40, pady=30)
        
        form = tk.Frame(self.content, bg="#0a0a0a")
        form.pack(fill=tk.BOTH, expand=True, padx=40)
        
        tk.Label(form, text="World Name", bg="#0a0a0a", fg="#666").pack(anchor="w")
        name_ent = tk.Entry(form, width=60, font=("Segoe UI", 12), bg="#111", fg="white")
        name_ent.insert(0, self.engine.world.get("world_name", ""))
        name_ent.pack(pady=5, anchor="w")
        
        tk.Label(form, text="Lore Summary", bg="#0a0a0a", fg="#666").pack(anchor="w", pady=(10,0))
        hist_text = tk.Text(form, width=90, height=15, bg="#111", fg="white", font=("Segoe UI", 11))
        hist_text.insert("1.0", self.engine.world.get("history_summary", ""))
        hist_text.pack(pady=5, anchor="w")
        
        def save():
            self.engine.world["world_name"] = name_ent.get()
            self.engine.world["history_summary"] = hist_text.get("1.0", tk.END).strip()
            self.engine.save()
            messagebox.showinfo("Nexus", "World data synchronized.")
            
        tk.Button(form, text="SAVE WORLD DATA", command=save, bg="#007acc", fg="white", padx=30, pady=12, font=("Segoe UI", 10, "bold")).pack(pady=30, anchor="w")

    def show_editor(self):
        self.clear_content()
        StoryEditor(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_module_manager(self, mod_name):
        self.clear_content()
        ModuleManager(self.content, self.engine, self.ai, mod_name).pack(fill=tk.BOTH, expand=True)

    def show_ai_panel(self):
        self.clear_content()
        AIPanel(self.content, self.engine, self.ai).pack(fill=tk.BOTH, expand=True)

    def show_lore_wiki(self):
        self.clear_content()
        LoreWiki(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def export_project(self):
        if not self.engine.current_id: return
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {self.engine.config['project_name']}\n\n")
                f.write(f"Genre: {self.engine.config['genre']} | World: {self.engine.world['world_name']}\n\n")
                f.write("## WORLD LORE\n")
                f.write(self.engine.world['history_summary'] + "\n\n")
                f.write("## STORY\n")
                story_dir = os.path.join(self.engine.get_dir(), "story")
                for cfile in sorted(os.listdir(story_dir)):
                    if cfile.endswith(".txt"):
                        f.write(f"### {cfile.replace('.txt', '')}\n")
                        with open(os.path.join(story_dir, cfile), "r", encoding="utf-8") as cf:
                            f.write(cf.read() + "\n\n")
            messagebox.showinfo("Nexus", "Export Complete.")
