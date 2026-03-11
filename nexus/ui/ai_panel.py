import tkinter as tk
from tkinter import scrolledtext

class AIPanel(tk.Frame):
    """The Ultimate AI Interaction Panel for Gemini God Assistant."""
    def __init__(self, parent, engine, ai):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.ai = ai
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="🤖 AI GOD ASSISTANT", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(anchor="w", padx=40, pady=30)
        
        ai_frame = tk.Frame(self, bg="#0a0a0a")
        ai_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        self.prompt_ent = tk.Entry(ai_frame, width=100, font=("Segoe UI", 12), bg="#111", fg="white", borderwidth=0)
        self.prompt_ent.pack(pady=10, fill=tk.X)
        
        self.res_text = scrolledtext.ScrolledText(ai_frame, height=25, bg="#111", fg="white", font=("Segoe UI", 11), borderwidth=0)
        self.res_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        btn_row = tk.Frame(ai_frame, bg="#0a0a0a")
        btn_row.pack(pady=10, fill=tk.X)
        
        tk.Button(btn_row, text="INVOKE NEXUS", command=self.ask, bg="#00ff00", fg="black", font=("Segoe UI", 11, "bold"), padx=40, pady=12).pack(side=tk.LEFT)
        tk.Button(btn_row, text="CHECK CONSISTENCY", command=self.check_consistency, bg="#cc0000", fg="white", font=("Segoe UI", 11, "bold"), padx=40, pady=12).pack(side=tk.LEFT, padx=20)

    def ask(self):
        p = self.prompt_ent.get()
        if not p: return
        self.res_text.delete("1.0", tk.END)
        self.res_text.insert(tk.END, "Consulting the Nexus...")
        self.update()
        
        ctx = f"World: {self.engine.world['world_name']}\nGenre: {self.engine.config['genre']}\nLore: {self.engine.world['history_summary']}"
        response = self.ai.ask(p, ctx)
        self.res_text.delete("1.0", tk.END)
        self.res_text.insert(tk.END, response)

    def check_consistency(self):
        self.res_text.delete("1.0", tk.END)
        self.res_text.insert(tk.END, "Analyzing the Nexus for contradictions...")
        self.update()
        
        ctx = f"World: {self.engine.world['world_name']}\nGenre: {self.engine.config['genre']}\nLore: {self.engine.world['history_summary']}"
        response = self.ai.check_consistency(ctx)
        self.res_text.delete("1.0", tk.END)
        self.res_text.insert(tk.END, response)
