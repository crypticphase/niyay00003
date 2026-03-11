import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

class SnapshotManager(tk.Frame):
    """The Ultimate Snapshot & Versioning Manager."""
    def __init__(self, parent, engine):
        super().__init__(parent, bg="#0a0a0a")
        self.engine = engine
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0a0a0a")
        header.pack(fill=tk.X, padx=40, pady=30)
        tk.Label(header, text="📸 SNAPSHOTS", font=("Segoe UI", 28, "bold"), bg="#0a0a0a", fg="white").pack(side=tk.LEFT)
        
        main_frame = tk.Frame(self, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40)
        
        self.lb = tk.Listbox(main_frame, width=80, height=20, bg="#111", fg="#ccc", font=("Segoe UI", 11), borderwidth=0)
        self.lb.pack(side=tk.LEFT, fill=tk.Y)
        
        self.refresh_list()
        
        ctrl_frame = tk.Frame(main_frame, bg="#0a0a0a", padx=20)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Button(ctrl_frame, text="CAPTURE SNAPSHOT", command=self.capture, bg="#007acc", fg="white", width=20, pady=10).pack(pady=5)
        tk.Button(ctrl_frame, text="RESTORE SELECTED", command=self.restore, bg="#cc0000", fg="white", width=20, pady=10).pack(pady=5)

    def refresh_list(self):
        self.lb.delete(0, tk.END)
        snap_dir = os.path.join(self.engine.get_dir(), "snapshots")
        if os.path.exists(snap_dir):
            for s in sorted(os.listdir(snap_dir), reverse=True):
                self.lb.insert(tk.END, s)

    def capture(self):
        label = "Manual Snapshot"
        self.engine.create_snapshot(label)
        messagebox.showinfo("Nexus", "Snapshot captured successfully.")
        self.refresh_list()

    def restore(self):
        sel = self.lb.curselection()
        if not sel: return
        
        snap_id = self.lb.get(sel[0])
        if messagebox.askyesno("Nexus", f"Are you sure you want to restore {snap_id}? Current unsaved data will be lost."):
            # Restore logic (Simple version: copy files back)
            messagebox.showinfo("Nexus", "Restore feature is partially implemented. Please manually copy files from snapshot directory.")
