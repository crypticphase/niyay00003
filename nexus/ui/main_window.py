import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from nexus.engine.project_manager import ProjectManager
from nexus.engine.ai_connector import AIConnector
from nexus.ui.editor import StoryEditor
from nexus.ui.module_view import ModuleManager
from nexus.ui.ai_panel import AIPanel
from nexus.ui.wiki import LoreWiki
from nexus.ui.plot_planner import PlotPlanner
from nexus.ui.timeline import TimelineView
from fpdf import FPDF
from nexus.ui.snapshots import SnapshotManager
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
            ("🌍 ตั้งค่าโลก", self.show_world_config),
            ("📖 เขียนเนื้อเรื่อง", self.show_editor),
            ("🗺️ วางโครงเรื่อง", self.show_plot_planner),
            ("📜 เส้นเวลา", self.show_timeline),
            ("📚 คลังข้อมูล Lore", self.show_lore_wiki),
            ("🤖 ผู้ช่วย AI", self.show_ai_panel),
        ]
        
        if self.engine.current_id:
            tk.Label(self.nav_frame, text="หมวดหมู่ข้อมูล", font=("Segoe UI", 8, "bold"), bg="#111", fg="#444").pack(pady=(15, 5), anchor="w", padx=10)
            for mod in self.engine.config.get("modules", []):
                label = f"  {mod.replace('_', ' ').capitalize()}"
                nav_items.append((label, lambda m=mod: self.show_module_manager(m)))

        nav_items.append(("", None)) # Spacer
        nav_items.append(("📸 จุดบันทึก (Snapshots)", self.show_snapshots))
        nav_items.append(("📤 ส่งออก Markdown", self.export_project))
        nav_items.append(("📄 ส่งออก PDF", self.export_pdf))
        nav_items.append(("🏠 หน้าแรก", self.show_welcome))

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
        tk.Label(frame, text="สุดยอดเครื่องมือสร้างโลกและเขียนนิยายระดับพระเจ้า", font=("Segoe UI", 16), bg="#0a0a0a", fg="#666").pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg="#0a0a0a")
        btn_frame.pack(pady=40)
        
        tk.Button(btn_frame, text="สร้างโลกใหม่", command=self.dialog_new_project, width=25, bg="#007acc", fg="white", pady=12, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="โหลดโลกเดิม", command=self.dialog_load_project, width=25, bg="#222", fg="white", pady=12, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)

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
        self.clear_content()
        self.update_sidebar()
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
        StoryEditor(self.content, self.engine, self.ai).pack(fill=tk.BOTH, expand=True)

    def show_module_manager(self, mod_name):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        ModuleManager(self.content, self.engine, self.ai, mod_name).pack(fill=tk.BOTH, expand=True)

    def show_ai_panel(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        AIPanel(self.content, self.engine, self.ai).pack(fill=tk.BOTH, expand=True)

    def show_lore_wiki(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        LoreWiki(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_plot_planner(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        PlotPlanner(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_timeline(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        TimelineView(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

    def show_snapshots(self):
        if not self.engine.current_id:
            messagebox.showwarning("Nexus", "Please load or create a project first.")
            self.show_welcome()
            return
        self.clear_content()
        SnapshotManager(self.content, self.engine).pack(fill=tk.BOTH, expand=True)

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
