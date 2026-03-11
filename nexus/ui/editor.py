import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

class StoryEditor(tk.Frame):
    """The Ultimate Rich Text Editor for writing stories with Focus Mode and Goals."""
    def __init__(self, parent, engine, ai):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.ai = ai
        self.focus_mode = False
        self.setup_ui()
        self.load_chapter()

    def setup_ui(self):
        self.header = tk.Frame(self, bg="#0a0a0a")
        self.header.pack(fill=tk.X, padx=40, pady=20)
        
        tk.Label(self.header, text="📖 เขียนเนื้อเรื่อง", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        btn_row = tk.Frame(self.header, bg="#0a0a0a")
        btn_row.pack(side=tk.RIGHT)
        
        # AI Tools Row
        ai_tools = tk.Frame(self, bg="#111", pady=5)
        ai_tools.pack(fill=tk.X, padx=40)
        
        tk.Button(ai_tools, text="✨ เขียนต่อ", command=self.ai_continue, bg="#8a2be2", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(ai_tools, text="✍️ เกลาใหม่", command=self.ai_rewrite, bg="#4b0082", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(ai_tools, text="🔍 ขยายความ", command=self.ai_expand, bg="#6a5acd", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(ai_tools, text="📊 วิเคราะห์เรื่อง", command=self.ai_analyze, bg="#333", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(ai_tools, text="🎯 โหมดโฟกัส", command=self.toggle_focus, bg="#222", fg="#888", padx=10).pack(side=tk.RIGHT, padx=5)
        
        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Georgia", 14), bg="#0f0f0f", fg="#bbb", insertbackground="white", padx=50, pady=50, borderwidth=0, undo=True)
        self.text.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        self.text.bind("<KeyRelease>", self.on_key_release)
        
        self.footer = tk.Frame(self, bg="#0a0a0a")
        self.footer.pack(fill=tk.X, padx=40, pady=10)
        
        self.stats = tk.Label(self.footer, text="จำนวนคำ: 0", bg="#0a0a0a", fg="#666", font=("Segoe UI", 10))
        self.stats.pack(side=tk.RIGHT)
        
        self.goal_lbl = tk.Label(self.footer, text=f"เป้าหมาย: {self.engine.config.get('word_goal', 50000)}", bg="#0a0a0a", fg="#666", font=("Segoe UI", 10))
        self.goal_lbl.pack(side=tk.LEFT)

    def on_key_release(self, event):
        self.update_stats()
        if event.char == "@":
            self.show_mention_popup()

    def show_mention_popup(self):
        # Get cursor position in pixels
        pos = self.text.bbox(tk.INSERT)
        if not pos: return
        
        win = tk.Toplevel(self)
        win.overrideredirect(True) # No title bar
        win.geometry(f"200x300+{self.winfo_rootx() + pos[0] + 50}+{self.winfo_rooty() + pos[1] + 150}")
        win.configure(bg="#1a1a1a")
        
        lb = tk.Listbox(win, bg="#1a1a1a", fg="#00ff00", borderwidth=0, highlightthickness=0)
        lb.pack(fill=tk.BOTH, expand=True)
        
        all_items = []
        for m, items in self.engine.modules.items():
            for it in items:
                all_items.append(f"{m}:{it.get('name')}")
        
        for item in all_items:
            lb.insert(tk.END, item)
            
        def select(evt=None):
            if lb.curselection():
                val = lb.get(lb.curselection())
                # Replace @ with link
                self.text.delete("insert-1c", "insert")
                self.text.insert(tk.INSERT, f"[[{val}]]")
                win.destroy()
        
        lb.bind("<Double-Button-1>", select)
        lb.bind("<Return>", select)
        win.bind("<Escape>", lambda e: win.destroy())
        lb.focus_set()

    def toggle_focus(self):
        self.focus_mode = not self.focus_mode
        if self.focus_mode:
            self.header.pack_forget()
            self.footer.pack_forget()
            self.text.pack_configure(padx=200)
            messagebox.showinfo("Nexus", "Focus Mode Enabled. Press ESC to exit (Not implemented, use button).")
        else:
            self.header.pack(fill=tk.X, padx=40, pady=20, before=self.text)
            self.footer.pack(fill=tk.X, padx=40, pady=10)
            self.text.pack_configure(padx=40)

    def load_chapter(self):
        if not self.engine.current_id: return
        chapter_file = os.path.join(self.engine.get_dir(), "story", f"{self.engine.config.get('active_chapter', 'chapter_01')}.txt")
        if os.path.exists(chapter_file):
            with open(chapter_file, "r", encoding="utf-8") as f:
                self.text.insert("1.0", f.read())
        self.update_stats()
        self.auto_save()

    def update_stats(self, evt=None):
        content = self.text.get("1.0", tk.END).strip()
        words = len(content.split())
        self.stats.config(text=f"จำนวนคำ: {words}")
        
        # Progress color
        goal = self.engine.config.get('word_goal', 50000)
        if words >= goal: self.stats.config(fg="#00ff00")

    def ai_analyze(self):
        content = self.text.get("1.0", tk.END).strip()
        if not content: return
        ctx = f"World: {self.engine.world['world_name']}\nLore: {self.engine.world['history_summary']}"
        res = self.ai.analyze_story_director(content, ctx)
        self.show_ai_result("AI Story Director Analysis", res)

    def ai_continue(self):
        content = self.text.get("1.0", tk.END).strip()
        ctx = f"World: {self.engine.world['world_name']}\nLore: {self.engine.world['history_summary']}"
        res = self.ai.continue_story(content[-2000:], ctx) # Send last 2000 chars
        self.text.insert(tk.END, f"\n\n{res}")

    def ai_rewrite(self):
        try:
            selected = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            messagebox.showwarning("Nexus", "กรุณาคลุมดำข้อความที่ต้องการเกลาใหม่")
            return
        
        ctx = f"World: {self.engine.world['world_name']}\nLore: {self.engine.world['history_summary']}"
        res = self.ai.rewrite_story(selected, "เกลาให้สละสลวยและเห็นภาพชัดเจน", ctx)
        
        self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.text.insert(tk.INSERT, res)

    def ai_expand(self):
        try:
            selected = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            selected = self.text.get("insert linestart", "insert lineend")
            
        ctx = f"World: {self.engine.world['world_name']}\nLore: {self.engine.world['history_summary']}"
        res = self.ai.expand_story(selected, ctx)
        self.show_ai_result("AI Expansion", res)

    def show_ai_result(self, title, content):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("600x500")
        txt = scrolledtext.ScrolledText(win, bg="#111", fg="white", font=("Segoe UI", 11))
        txt.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        txt.insert(tk.END, content)

    def auto_save(self):
        if self.engine.current_id:
            chapter_file = os.path.join(self.engine.get_dir(), "story", f"{self.engine.config.get('active_chapter', 'chapter_01')}.txt")
            with open(chapter_file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END).strip())
            self.after(10000, self.auto_save)
