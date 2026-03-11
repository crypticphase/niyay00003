import tkinter as tk
from tkinter import ttk, messagebox

class CalendarView(tk.Frame):
    """The Ultimate In-World Calendar System."""
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0a0a0a")
        header.pack(fill=tk.X, padx=40, pady=30)
        tk.Label(header, text="📅 IN-WORLD CALENDAR", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        main_frame = tk.Frame(self, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        # Calendar Settings
        settings = tk.Frame(main_frame, bg="#111", padx=20, pady=20)
        settings.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(settings, text="ปีปัจจุบัน:", bg="#111", fg="#888").pack(anchor="w")
        self.year_ent = tk.Entry(settings, width=10)
        self.year_ent.insert(0, str(self.engine.calendar.get("current_year", 1000)))
        self.year_ent.pack(pady=5)
        
        tk.Label(settings, text="จำนวนวันต่อสัปดาห์:", bg="#111", fg="#888").pack(anchor="w")
        self.days_ent = tk.Entry(settings, width=10)
        self.days_ent.insert(0, str(self.engine.calendar.get("days_per_week", 7)))
        self.days_ent.pack(pady=5)
        
        tk.Label(settings, text="รายชื่อเดือน (คั่นด้วยคอมม่า):", bg="#111", fg="#888").pack(anchor="w", pady=(10,0))
        self.months_ent = tk.Entry(settings, width=30)
        self.months_ent.insert(0, ", ".join(self.engine.calendar.get("months", [])))
        self.months_ent.pack(pady=5)
        
        tk.Button(settings, text="บันทึกปฏิทิน", command=self.save_cal, bg="#007acc", fg="white", pady=10).pack(pady=20, fill=tk.X)
        
        # Preview Area
        preview = tk.Frame(main_frame, bg="#0a0a0a", padx=40)
        preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(preview, text="ตัวอย่างปฏิทิน", font=("Segoe UI", 16), bg="#0a0a0a", fg="#666").pack(anchor="w")
        
        self.prev_area = tk.Frame(preview, bg="#0a0a0a")
        self.prev_area.pack(fill=tk.BOTH, expand=True, pady=20)
        self.render_preview()

    def render_preview(self):
        for w in self.prev_area.winfo_children(): w.destroy()
        months = self.engine.calendar.get("months", [])
        for i, m in enumerate(months):
            f = tk.Frame(self.prev_area, bg="#1a1a1a", padx=10, pady=10, borderwidth=1, relief=tk.SOLID)
            f.grid(row=i//4, column=i%4, padx=5, pady=5)
            tk.Label(f, text=m, bg="#1a1a1a", fg="#00ff00", font=("Segoe UI", 10, "bold")).pack()
            tk.Label(f, text="30 Days", bg="#1a1a1a", fg="#666", font=("Segoe UI", 8)).pack()

    def save_cal(self):
        try:
            self.engine.calendar["current_year"] = int(self.year_ent.get())
            self.engine.calendar["days_per_week"] = int(self.days_ent.get())
            self.engine.calendar["months"] = [m.strip() for m in self.months_ent.get().split(",") if m.strip()]
            self.engine.save()
            self.render_preview()
            messagebox.showinfo("Nexus", "บันทึกปฏิทินเรียบร้อยแล้ว")
        except ValueError:
            messagebox.showerror("Nexus", "กรุณากรอกตัวเลขให้ถูกต้อง")
