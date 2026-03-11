import tkinter as tk
from tkinter import scrolledtext
import os

class StoryEditor(tk.Frame):
    """Rich Text Editor for writing stories with auto-save."""
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()
        self.load_chapter()

    def setup_ui(self):
        tk.Label(self, text="📖 STORY EDITOR", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(anchor="w", padx=40, pady=30)
        
        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Georgia", 14), bg="#0f0f0f", fg="#bbb", insertbackground="white", padx=50, pady=50, borderwidth=0, undo=True)
        self.text.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        self.stats = tk.Label(self, text="Words: 0", bg="#0a0a0a", fg="#666", font=("Segoe UI", 10))
        self.stats.pack(anchor="e", padx=50, pady=10)
        
        self.text.bind("<KeyRelease>", self.update_stats)

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
        self.stats.config(text=f"Words: {words} / {self.engine.config.get('word_goal', 50000)}")

    def auto_save(self):
        if self.engine.current_id:
            chapter_file = os.path.join(self.engine.get_dir(), "story", f"{self.engine.config.get('active_chapter', 'chapter_01')}.txt")
            with open(chapter_file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END).strip())
            self.after(10000, self.auto_save)
