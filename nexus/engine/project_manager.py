import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class ProjectManager:
    """Handles the lifecycle of a Nexus project and its data storage."""
    def __init__(self, base_path: str = "projects"):
        self.base_path = base_path
        self.current_id = None
        self.config = {}
        self.world = {}
        self.modules = {}
        self.plot = {"acts": []}
        
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def get_dir(self):
        return os.path.join(self.base_path, self.current_id) if self.current_id else None

    def create(self, name: str, genre: str, world_type: str):
        self.current_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        p_dir = self.get_dir()
        
        os.makedirs(p_dir)
        os.makedirs(os.path.join(p_dir, "modules"))
        os.makedirs(os.path.join(p_dir, "story"))
        os.makedirs(os.path.join(p_dir, "lore"))
        os.makedirs(os.path.join(p_dir, "snapshots"))
        
        # Default Modules
        mods = ["characters", "history", "items", "kingdoms", "factions", "magic_system", "planets"]
        
        self.config = {
            "project_id": self.current_id,
            "project_name": name,
            "genre": genre,
            "world_type": world_type,
            "created_at": datetime.now().isoformat(),
            "modules": mods,
            "active_chapter": "chapter_01",
            "word_goal": 50000
        }
        
        self.world = {
            "world_name": f"New {world_type.capitalize()} World",
            "theme": "General",
            "magic_system": {"exists": True, "rules": ""},
            "history_summary": "",
            "geography": ""
        }

        self.plot = {"acts": [{"title": "Act I", "scenes": [{"title": "Opening", "status": "Draft"}]}]}
        self.modules = {m: [] for m in mods}
        
        self.save()
        return self.current_id

    def load(self, proj_id: str):
        p_dir = os.path.join(self.base_path, proj_id)
        with open(os.path.join(p_dir, "config.json"), "r", encoding="utf-8") as f:
            self.config = json.load(f)
        with open(os.path.join(p_dir, "world.json"), "r", encoding="utf-8") as f:
            self.world = json.load(f)
        
        plot_path = os.path.join(p_dir, "story", "plot.json")
        if os.path.exists(plot_path):
            with open(plot_path, "r", encoding="utf-8") as f:
                self.plot = json.load(f)
        
        self.current_id = proj_id
        self.modules = {}
        for mod in self.config.get("modules", []):
            path = os.path.join(p_dir, "modules", f"{mod}.json")
            self.modules[mod] = json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else []
        return True

    def save(self):
        if not self.current_id: return
        p_dir = self.get_dir()
        
        files = [
            ("config.json", self.config),
            ("world.json", self.world),
            (os.path.join("story", "plot.json"), self.plot)
        ]
        
        for filename, data in files:
            with open(os.path.join(p_dir, filename), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        for mod, data in self.modules.items():
            path = os.path.join(p_dir, "modules", f"{mod}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
