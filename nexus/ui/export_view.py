import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from fpdf import FPDF

class ExportManager(tk.Frame):
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="📤 ระบบส่งออกเนื้อเรื่อง (Export System)", font=("Segoe UI", 24, "bold"), bg="#0a0a0a", fg="white").pack(pady=20)
        
        main_frame = tk.Frame(self, bg="#111", padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        # Left: Chapter Selection
        left_frame = tk.Frame(main_frame, bg="#111")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text="เลือกบทที่ต้องการส่งออก:", bg="#111", fg="#888", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        self.chapter_list = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, bg="#222", fg="white", font=("Segoe UI", 11), borderwidth=0, highlightthickness=0)
        self.chapter_list.pack(fill=tk.BOTH, expand=True, pady=10)
        
        story_dir = os.path.join(self.engine.get_dir(), "story")
        if os.path.exists(story_dir):
            for f in sorted(os.listdir(story_dir)):
                if f.endswith(".txt"):
                    self.chapter_list.insert(tk.END, f.replace(".txt", ""))
        
        # Select All / None
        btn_sel_frame = tk.Frame(left_frame, bg="#111")
        btn_sel_frame.pack(fill=tk.X)
        tk.Button(btn_sel_frame, text="เลือกทั้งหมด", command=lambda: self.chapter_list.select_set(0, tk.END), bg="#333", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_sel_frame, text="ไม่เลือกเลย", command=lambda: self.chapter_list.select_clear(0, tk.END), bg="#333", fg="white").pack(side=tk.LEFT, padx=5)

        # Right: Options
        right_frame = tk.Frame(main_frame, bg="#111", padx=20)
        right_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(right_frame, text="รูปแบบไฟล์:", bg="#111", fg="#888", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.format_var = tk.StringVar(value="PDF")
        formats = [("PDF Document (.pdf)", "PDF"), ("Microsoft Word (.docx) - Coming Soon", "DOCX"), ("Markdown (.md)", "MD"), ("Plain Text (.txt)", "TXT")]
        for text, val in formats:
            state = tk.NORMAL if val != "DOCX" else tk.DISABLED
            tk.Radiobutton(right_frame, text=text, variable=self.format_var, value=val, bg="#111", fg="white", selectcolor="#007acc", activebackground="#111", activeforeground="white", state=state).pack(anchor="w", pady=5)

        tk.Label(right_frame, text="ตัวเลือกเพิ่มเติม:", bg="#111", fg="#888", font=("Segoe UI", 10, "bold"), pady=15).pack(anchor="w")
        self.include_lore = tk.BooleanVar(value=True)
        tk.Checkbutton(right_frame, text="รวมข้อมูล Lore (World Config)", variable=self.include_lore, bg="#111", fg="white", selectcolor="#007acc", activebackground="#111", activeforeground="white").pack(anchor="w")
        
        self.include_notes = tk.BooleanVar(value=False)
        tk.Checkbutton(right_frame, text="รวม Scene Notes (ถ้ามี)", variable=self.include_notes, bg="#111", fg="white", selectcolor="#007acc", activebackground="#111", activeforeground="white").pack(anchor="w")

        # Export Button
        tk.Button(right_frame, text="🚀 เริ่มการส่งออก", command=self.start_export, bg="#007acc", fg="white", font=("Segoe UI", 12, "bold"), pady=15).pack(fill=tk.X, pady=30)

    def start_export(self):
        selected_indices = self.chapter_list.curselection()
        if not selected_indices:
            messagebox.showwarning("Export", "กรุณาเลือกบทที่ต้องการส่งออกอย่างน้อย 1 บท")
            return
        
        selected_chapters = [self.chapter_list.get(i) for i in selected_indices]
        fmt = self.format_var.get()
        
        if fmt == "PDF":
            self.export_pdf(selected_chapters)
        elif fmt == "MD":
            self.export_md(selected_chapters)
        elif fmt == "TXT":
            self.export_txt(selected_chapters)

    def export_pdf(self, chapters):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not file_path: return
        
        try:
            pdf = FPDF()
            pdf.add_page()
            # Use a font that supports Thai if possible, but for now stick to standard
            pdf.set_font("Arial", 'B', 24)
            pdf.cell(0, 20, txt=self.engine.config['project_name'], ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, txt=f"Genre: {self.engine.config['genre']}", ln=True, align='C')
            pdf.ln(20)

            if self.include_lore.get():
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, txt="World Lore", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=self.engine.world.get('history_summary', ''))
                pdf.ln(10)

            story_dir = os.path.join(self.engine.get_dir(), "story")
            for chap in chapters:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 18)
                pdf.cell(0, 15, txt=chap, ln=True)
                pdf.set_font("Arial", size=12)
                
                path = os.path.join(story_dir, f"{chap}.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # FPDF doesn't handle unicode well without custom fonts
                        # For now, we'll just try to write it
                        pdf.multi_cell(0, 10, txt=content)
            
            pdf.output(file_path)
            messagebox.showinfo("Export", "ส่งออก PDF สำเร็จ!")
        except Exception as e:
            messagebox.showerror("Export Error", f"เกิดข้อผิดพลาดในการส่งออก PDF: {str(e)}")

    def export_md(self, chapters):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md")])
        if not file_path: return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {self.engine.config['project_name']}\n\n")
                f.write(f"**Genre:** {self.engine.config['genre']}\n\n")
                
                if self.include_lore.get():
                    f.write("## World Lore\n")
                    f.write(self.engine.world.get('history_summary', '') + "\n\n")
                
                story_dir = os.path.join(self.engine.get_dir(), "story")
                for chap in chapters:
                    f.write(f"## {chap}\n\n")
                    path = os.path.join(story_dir, f"{chap}.txt")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as cf:
                            f.write(cf.read() + "\n\n")
            
            messagebox.showinfo("Export", "ส่งออก Markdown สำเร็จ!")
        except Exception as e:
            messagebox.showerror("Export Error", f"เกิดข้อผิดพลาดในการส่งออก Markdown: {str(e)}")

    def export_txt(self, chapters):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if not file_path: return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{self.engine.config['project_name']}\n")
                f.write("="*len(self.engine.config['project_name']) + "\n\n")
                
                story_dir = os.path.join(self.engine.get_dir(), "story")
                for chap in chapters:
                    f.write(f"--- {chap} ---\n\n")
                    path = os.path.join(story_dir, f"{chap}.txt")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as cf:
                            f.write(cf.read() + "\n\n")
            
            messagebox.showinfo("Export", "ส่งออก Text สำเร็จ!")
        except Exception as e:
            messagebox.showerror("Export Error", f"เกิดข้อผิดพลาดในการส่งออก Text: {str(e)}")
