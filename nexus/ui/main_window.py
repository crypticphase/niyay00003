import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
from nexus.engine.project_manager import ProjectManager
from nexus.engine.ai_connector import AIConnector
from nexus.ui.editor import StoryEditor
from nexus.ui.module_view import ModuleManager
from nexus.ui.ai_panel import AIPanel
from nexus.ui.wiki import LoreWiki
from nexus.ui.plot_planner import PlotPlanner
from nexus.ui.timeline import TimelineView
from nexus.ui.calendar import CalendarView
from fpdf import FPDF
from nexus.ui.snapshots import SnapshotManager
from nexus.ui.export_view import ExportManager
from nexus.ui.search_view import GlobalSearch
import os

class MainWindow(tk.Tk):
    """The Ultimate Application Window for Nexus God Writer."""
    def __init__(self):
        super().__init__()
        self.title("NEXUS GOD WRITER - สุดยอดเครื่องมือสร้างโลกและเขียนนิยาย")
        self.geometry("1400x900")
        self.configure(bg="#0a0a0a")
        
        self.engine = ProjectManager()
        self.ai = AIConnector()
        
        self.bind("<Control-k>", lambda e: self.show_command_palette())
        self.bind("<Control-K>", lambda e: self.show_command_palette())
        self.bind("<Control-f>", lambda e: self.show_global_search())
        self.bind("<Control-F>", lambda e: self.show_global_search())
        self.bind("<Control-space>", lambda e: self.show_quick_capture())
        
        self.setup_layout()
        self.show_welcome()

    def show_quick_capture(self):
        win = tk.Toplevel(self)
        win.title("Quick Capture")
        win.geometry("400x250")
        win.configure(bg="#111", padx=20, pady=20)
        win.transient(self)
        
        tk.Label(win, text="💡 จดไอเดียด่วน (Quick Capture)", bg="#111", fg="#00ff00", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        txt = tk.Text(win, height=5, bg="#222", fg="white", font=("Segoe UI", 11), borderwidth=0, insertbackground="white")
        txt.pack(fill=tk.BOTH, expand=True, pady=10)
        txt.focus_set()
        
        def save():
            note = txt.get("1.0", tk.END).strip()
            if note:
                self.engine.facts.append({"content": note, "type": "quick_capture", "date": datetime.now().isoformat()})
                self.engine.save()
                messagebox.showinfo("Nexus", "บันทึกไอเดียลงใน Inbox แล้ว")
            win.destroy()
            
        tk.Button(win, text="บันทึก (Enter)", command=save, bg="#007acc", fg="white", padx=20).pack(side=tk.RIGHT)
        win.bind("<Return>", lambda e: save())
        win.bind("<Escape>", lambda e: win.destroy())

    def show_command_palette(self):
        win = tk.Toplevel(self)
        win.title("Command Palette")
        win.geometry("500x400")
        win.configure(bg="#111", padx=10, pady=10)
        win.transient(self)
        win.grab_set()
        
        tk.Label(win, text="COMMAND PALETTE (ค้นหาหรือสั่งการ)", bg="#111", fg="#00ff00", font=("Segoe UI", 10, "bold")).pack(pady=5)
        
        search_ent = tk.Entry(win, font=("Segoe UI", 14), bg="#222", fg="white", borderwidth=0, insertbackground="white")
        search_ent.pack(fill=tk.X, pady=10)
        search_ent.focus_set()
        
        results_frame = tk.Frame(win, bg="#111")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        def do_search(evt=None):
            for w in results_frame.winfo_children(): w.destroy()
            term = search_ent.get().lower()
            if not term: return
            
            # Commands
            commands = [
                ("🌍 ไปที่: ตั้งค่าโลก", self.show_world_config),
                ("📖 ไปที่: เขียนเนื้อเรื่อง", self.show_editor),
                ("🔍 ค้นหาข้ามโปรเจกต์", self.show_global_search),
                ("🤖 ไปที่: ผู้ช่วย AI", self.show_ai_panel),
                ("📅 ไปที่: ปฏิทิน", self.show_calendar),
                ("💾 บันทึกโปรเจกต์", self.engine.save),
            ]
            
            for text, cmd in commands:
                if term in text.lower():
                    btn = tk.Button(results_frame, text=text, command=lambda c=cmd: [c(), win.destroy()], 
                                    bg="#222", fg="#ccc", anchor="w", relief=tk.FLAT, pady=5)
                    btn.pack(fill=tk.X, pady=1)

            # Recently Viewed
            if self.engine.recently_viewed:
                tk.Label(results_frame, text="RECENTLY VIEWED", bg="#111", fg="#444", font=("Segoe UI", 8)).pack(pady=5, anchor="w")
                for r in self.engine.recently_viewed:
                    if term in r["name"].lower():
                        def go(item=r):
                            if item["type"] == "nav":
                                # This is tricky since we need to map names to functions
                                # For now, let's just search lore
                                pass
                            elif item["type"] == "module":
                                self.show_module_manager(item["data"])
                            win.destroy()
                        
                        btn = tk.Button(results_frame, text=f"🕒 {r['name']}", command=go,
                                        bg="#1a1a1a", fg="#666", anchor="w", relief=tk.FLAT, pady=5)
                        btn.pack(fill=tk.X, pady=1)

            # Lore Entries
            if self.engine.current_id:
                for mod, items in self.engine.modules.items():
                    for it in items:
                        name = it.get("name", "Unnamed")
                        if term in name.lower():
                            btn = tk.Button(results_frame, text=f"📦 {mod.upper()}: {name}", 
                                            command=lambda m=mod: [self.show_module_manager(m), win.destroy()],
                                            bg="#1a1a1a", fg="#888", anchor="w", relief=tk.FLAT, pady=5)
                            btn.pack(fill=tk.X, pady=1)

        search_ent.bind("<KeyRelease>", do_search)
        win.bind("<Escape>", lambda e: win.destroy())

    def setup_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, width=250, bg="#111", padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="NEXUS", font=("Impact", 28), bg="#111", fg="#00ff00").pack(pady=20)
        
        tk.Button(self.sidebar, text="🔍 COMMAND PALETTE (Ctrl+K)", command=self.show_command_palette, 
                  bg="#222", fg="#00ff00", font=("Segoe UI", 8, "bold"), pady=5).pack(fill=tk.X, pady=10)
        
        self.nav_frame = tk.Frame(self.sidebar, bg="#111")
        self.nav_frame.pack(fill=tk.BOTH, expand=True)

        # Content Area with Breadcrumb
        self.main_container = tk.Frame(self, bg="#0a0a0a")
        self.main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.breadcrumb_bar = tk.Frame(self.main_container, bg="#0f0f0f", height=40)
        self.breadcrumb_bar.pack(fill=tk.X)
        self.breadcrumb_bar.pack_propagate(False)
        
        self.content = tk.Frame(self.main_container, bg="#0a0a0a")
        self.content.pack(fill=tk.BOTH, expand=True)

    def update_breadcrumb(self, path_list):
        for w in self.breadcrumb_bar.winfo_children(): w.destroy()
        
        tk.Label(self.breadcrumb_bar, text="📍", bg="#0f0f0f", fg="#444").pack(side=tk.LEFT, padx=(10, 5))
        
        for i, item in enumerate(path_list):
            name, cmd = item
            btn = tk.Button(self.breadcrumb_bar, text=name, command=cmd, bg="#0f0f0f", fg="#888", 
                            relief=tk.FLAT, font=("Segoe UI", 9), activebackground="#1a1a1a", activeforeground="white")
            btn.pack(side=tk.LEFT)
            if i < len(path_list) - 1:
                tk.Label(self.breadcrumb_bar, text=">", bg="#0f0f0f", fg="#333").pack(side=tk.LEFT)

    def add_to_recent(self, name, cmd_type, data=None):
        entry = {"name": name, "type": cmd_type, "data": data}
        # Remove duplicate
        self.engine.recently_viewed = [r for r in self.engine.recently_viewed if r["name"] != name]
        self.engine.recently_viewed.insert(0, entry)
        self.engine.recently_viewed = self.engine.recently_viewed[:15] # Keep 15
        self.engine.save()

    def update_sidebar(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
            
        nav_items = [
            ("🌍 ตั้งค่าโลก", self.show_world_config),
            ("📖 เขียนเนื้อเรื่อง", self.show_editor),
            ("🗺️ วางโครงเรื่อง", self.show_plot_planner),
            ("📜 เส้นเวลา", self.show_timeline),
            ("📅 ปฏิทินโลก", self.show_calendar),
            ("📚 คลังข้อมูล Lore", self.show_lore_wiki),
            ("🤖 ผู้ช่วย AI", self.show_ai_panel),
        ]
        
        for text, cmd in nav_items:
            btn = tk.Button(self.nav_frame, text=text, command=cmd, bg="#111", fg="#ccc", 
                            relief=tk.FLAT, anchor="w", padx=15, pady=8, font=("Segoe UI", 10, "bold"),
                            activebackground="#222", activeforeground="white")
            btn.pack(fill=tk.X)

        if self.engine.current_id:
            tk.Label(self.nav_frame, text="คลังข้อมูล (LORE)", font=("Segoe UI", 8, "bold"), bg="#111", fg="#444").pack(pady=(15, 5), anchor="w", padx=10)
            for mod in self.engine.config.get("modules", []):
                label = f"  • {mod.replace('_', ' ').capitalize()}"
                btn = tk.Button(self.nav_frame, text=label, command=lambda m=mod: self.show_module_manager(m), 
                                bg="#111", fg="#888", relief=tk.FLAT, anchor="w", padx=20, pady=5, font=("Segoe UI", 9),
                                activebackground="#1a1a1a", activeforeground="#00ff00")
                btn.pack(fill=tk.X)

        tk.Frame(self.nav_frame, height=1, bg="#222").pack(fill=tk.X, pady=10)
        
        bottom_items = [
            ("📸 จุดบันทึก (Snapshots)", self.show_snapshots),
            ("📤 ส่งออกเนื้อเรื่อง", self.show_export_manager),
            ("🔍 ค้นหาข้ามโปรเจกต์", self.show_global_search),
            ("🏠 หน้าแรก", self.show_welcome)
        ]
        
        for text, cmd in bottom_items:
            btn = tk.Button(self.nav_frame, text=text, command=cmd, bg="#111", fg="#666", 
                            relief=tk.FLAT, anchor="w", padx=15, pady=5, font=("Segoe UI", 9),
                            activebackground="#222", activeforeground="white")
            btn.pack(fill=tk.X)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_content()
        self.update_sidebar()
        self.update_breadcrumb([("Home", self.show_welcome)])
        
        frame = tk.Frame(self.content, bg="#0a0a0a")
        frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        tk.Label(frame, text="NEXUS GOD WRITER", font=("Impact", 56), bg="#0a0a0a", fg="white").pack()
        tk.Label(frame, text="สุดยอดเครื่องมือสร้างโลกและเขียนนิยายระดับพระเจ้า", font=("Segoe UI", 16), bg="#0a0a0a", fg="#666").pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg="#0a0a0a")
        btn_frame.pack(pady=40)
        
        tk.Button(btn_frame, text="สร้างโลกใหม่ (Wizard)", command=self.show_onboarding, width=25, bg="#007acc", fg="white", pady=12, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="โหลดโลกเดิม", command=self.dialog_load_project, width=25, bg="#222", fg="white", pady=12, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)

    def show_onboarding(self):
        win = tk.Toplevel(self)
        win.title("Nexus Onboarding Wizard")
        win.geometry("500x600")
        win.configure(bg="#111", padx=30, pady=30)
        
        step = tk.IntVar(value=1)
        
        def next_step():
            if step.get() == 1:
                # Step 1: Name & Genre
                name = name_ent.get()
                genre = genre_var.get()
                if not name: return
                self.engine.create(name, genre, "Standard")
                step.set(2)
                render()
            elif step.get() == 2:
                # Step 2: World Theme
                self.engine.world["theme"] = theme_ent.get()
                self.engine.world["history_summary"] = hist_ent.get("1.0", tk.END)
                self.engine.save()
                step.set(3)
                render()
            else:
                win.destroy()
                self.show_welcome()

        def render():
            for w in win.winfo_children(): w.destroy()
            if step.get() == 1:
                tk.Label(win, text="ขั้นที่ 1: พื้นฐานจักรวาล", font=("Segoe UI", 18, "bold"), bg="#111", fg="#00ff00").pack(pady=20)
                tk.Label(win, text="ชื่อโลกของคุณ:", bg="#111", fg="white").pack(anchor="w")
                nonlocal name_ent
                name_ent = tk.Entry(win, font=("Segoe UI", 12))
                name_ent.pack(fill=tk.X, pady=10)
                
                tk.Label(win, text="แนวเรื่อง (Genre):", bg="#111", fg="white").pack(anchor="w")
                nonlocal genre_var
                genre_var = tk.StringVar(value="Fantasy")
                for g in ["Fantasy", "Sci-Fi", "Mystery", "Horror"]:
                    tk.Radiobutton(win, text=g, variable=genre_var, value=g, bg="#111", fg="white", selectcolor="#222").pack(anchor="w")
                
            elif step.get() == 2:
                tk.Label(win, text="ขั้นที่ 2: จิตวิญญาณของโลก", font=("Segoe UI", 18, "bold"), bg="#111", fg="#00ff00").pack(pady=20)
                tk.Label(win, text="ธีมหลัก (เช่น ความหวัง, การล่มสลาย):", bg="#111", fg="white").pack(anchor="w")
                nonlocal theme_ent
                theme_ent = tk.Entry(win, font=("Segoe UI", 12))
                theme_ent.pack(fill=tk.X, pady=10)
                
                tk.Label(win, text="ประวัติศาสตร์ย่อ:", bg="#111", fg="white").pack(anchor="w")
                nonlocal hist_ent
                hist_ent = tk.Text(win, height=5, font=("Segoe UI", 11))
                hist_ent.pack(fill=tk.X, pady=10)

            tk.Button(win, text="ถัดไป ->", command=next_step, bg="#007acc", fg="white", pady=10).pack(side=tk.BOTTOM, fill=tk.X)

        name_ent = None
        genre_var = None
        theme_ent = None
        hist_ent = None
        render()

    def dialog_new_project(self):
        win = tk.Toplevel(self)
        win.title("เริ่มต้นสร้างจักรวาลใหม่")
        win.geometry("450x500")
        win.configure(padx=30, pady=30, bg="#1a1a1a")
        
        tk.Label(win, text="ชื่อโปรเจกต์ / ชื่อเรื่อง", bg="#1a1a1a", fg="#888").pack(anchor="w")
        name_ent = tk.Entry(win, width=40, font=("Segoe UI", 11), bg="#222", fg="white")
        name_ent.pack(pady=5)
        
        tk.Label(win, text="แนวเรื่อง (Genre)", bg="#1a1a1a", fg="#888").pack(anchor="w", pady=(10,0))
        genre_ent = tk.Entry(win, width=40, font=("Segoe UI", 11), bg="#222", fg="white")
        genre_ent.pack(pady=5)
        
        tk.Label(win, text="ประเภทของโลก", bg="#1a1a1a", fg="#888").pack(anchor="w", pady=(10,0))
        wtype_var = tk.StringVar(value="fantasy")
        cb = ttk.Combobox(win, textvariable=wtype_var, values=["แฟนตาซี", "ไซไฟ", "ไซเบอร์พังค์", "สยองขวัญ", "โรแมนติก", "ประวัติศาสตร์"])
        cb.pack(pady=5, fill=tk.X)
        
        def create():
            if name_ent.get():
                self.engine.create(name_ent.get(), genre_ent.get(), wtype_var.get())
                win.destroy()
                self.show_world_config()
            else:
                messagebox.showwarning("Nexus", "กรุณาใส่ชื่อโปรเจกต์")
                
        tk.Button(win, text="สร้างโปรเจกต์", command=create, bg="#00ff00", fg="black", pady=12, font=("Segoe UI", 11, "bold")).pack(pady=30, fill=tk.X)

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
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("World Config", self.show_world_config)])
        self.add_to_recent("World Config", "nav")
        tk.Label(self.content, text="🌍 ตั้งค่าโลก (World Wizard)", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(anchor="w", padx=40, pady=30)
        
        form = tk.Frame(self.content, bg="#0a0a0a")
        form.pack(fill=tk.BOTH, expand=True, padx=40)
        
        tk.Label(form, text="ชื่อโลก / ชื่ออาณาจักร", bg="#0a0a0a", fg="#666").pack(anchor="w")
        name_ent = tk.Entry(form, width=60, font=("Segoe UI", 12), bg="#111", fg="white")
        name_ent.insert(0, self.engine.world.get("world_name", ""))
        name_ent.pack(pady=5, anchor="w")
        
        tk.Label(form, text="สรุปประวัติศาสตร์และข้อมูลเบื้องต้น", bg="#0a0a0a", fg="#666").pack(anchor="w", pady=(10,0))
        hist_text = tk.Text(form, width=90, height=15, bg="#111", fg="white", font=("Segoe UI", 11))
        hist_text.insert("1.0", self.engine.world.get("history_summary", ""))
        hist_text.pack(pady=5, anchor="w")
        
        def save():
            self.engine.world["world_name"] = name_ent.get()
            self.engine.world["history_summary"] = hist_text.get("1.0", tk.END).strip()
            self.engine.save()
            messagebox.showinfo("Nexus", "บันทึกข้อมูลโลกเรียบร้อยแล้ว")
            
        tk.Button(form, text="บันทึกข้อมูลโลก", command=save, bg="#007acc", fg="white", padx=30, pady=12, font=("Segoe UI", 10, "bold")).pack(pady=30, anchor="w")

    def show_editor(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Editor", self.show_editor)])
        self.add_to_recent("Editor", "nav")
        StoryEditor(self.content, self.engine, self.ai).pack(fill=tk.BOTH, expand=True)

    def show_module_manager(self, mod_name):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), (mod_name.capitalize(), lambda: self.show_module_manager(mod_name))])
        self.add_to_recent(f"Module: {mod_name}", "module", mod_name)
        ModuleManager(self.content, self.engine, self.ai, mod_name).pack(fill=tk.BOTH, expand=True)

    def show_ai_panel(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("AI Panel", self.show_ai_panel)])
        self.add_to_recent("AI Panel", "nav")
        AIPanel(self.content, self.engine, self.ai).pack(fill=tk.BOTH, expand=True)

    def show_lore_wiki(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Wiki", self.show_lore_wiki)])
        self.add_to_recent("Lore Wiki", "nav")
        LoreWiki(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_plot_planner(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Plot", self.show_plot_planner)])
        self.add_to_recent("Plot Planner", "nav")
        PlotPlanner(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_timeline(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Timeline", self.show_timeline)])
        self.add_to_recent("Timeline", "nav")
        TimelineView(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_calendar(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Calendar", self.show_calendar)])
        self.add_to_recent("Calendar", "nav")
        CalendarView(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_snapshots(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Snapshots", self.show_snapshots)])
        SnapshotManager(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_export_manager(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        self.update_breadcrumb([("Home", self.show_welcome), ("Export", self.show_export_manager)])
        ExportManager(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_global_search(self, evt=None):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            return
        GlobalSearch(self, self.engine)

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
    def export_pdf(self):
        if not self.engine.current_id: return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.cell(200, 10, txt=self.engine.config['project_name'], ln=True, align='C')
            pdf.ln(10)
            
            story_dir = os.path.join(self.engine.get_dir(), "story")
            for cfile in sorted(os.listdir(story_dir)):
                if cfile.endswith(".txt"):
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(200, 10, txt=cfile.replace('.txt', ''), ln=True)
                    pdf.set_font("Arial", size=12)
                    with open(os.path.join(story_dir, cfile), "r", encoding="utf-8") as cf:
                        pdf.multi_cell(0, 10, txt=cf.read())
                    pdf.ln(10)
            
            pdf.output(file_path)
            messagebox.showinfo("Nexus", "PDF Export Complete.")
