import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class ProjectManager:
    """The Ultimate Core Engine for Nexus God Writer."""
    def __init__(self, base_path: str = "projects"):
        self.base_path = base_path
        self.current_id = None
        self.config = {}
        self.world = {}
        self.modules = {}
        self.plot = {"acts": []}
        self.timeline = {"eras": []}
        self.calendar = {"months": [], "days_per_week": 7, "current_year": 1000}
        self.recently_viewed = []
        self.relations = []
        self.tags = []
        self.facts = []
        
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
        
        # Default Modules with Schema
        mods = ["characters", "locations", "history", "items", "kingdoms", "factions", "magic_system", "planets", "weapons"]
        
        self.config = {
            "project_id": self.current_id,
            "project_name": name,
            "genre": genre,
            "world_type": world_type,
            "created_at": datetime.now().isoformat(),
            "modules": mods,
            "active_chapter": "chapter_01",
            "word_goal": 50000,
            "daily_goal": 500,
            "schemas": {
                "characters": ["name", "age", "role", "personality", "abilities", "backstory"],
                "locations": ["name", "type", "parent_location", "description", "climate", "coordinates"],
                "weapons": ["name", "type", "owner", "power_level", "history"],
                "items": ["name", "type", "description", "owner"],
                "kingdoms": ["name", "ruler", "capital", "population", "description"]
            }
        }
        
        self.world = {
            "world_name": f"New {world_type.capitalize()} World",
            "theme": "General",
            "magic_system": {"exists": True, "rules": ""},
            "history_summary": "",
            "geography": "",
            "technology_level": "Medieval"
        }

        self.plot = {
            "acts": [
                {"title": "Act I: Setup", "scenes": [{"title": "Opening", "status": "Draft", "summary": ""}]},
                {"title": "Act II: Confrontation", "scenes": []},
                {"title": "Act III: Resolution", "scenes": []}
            ]
        }
        
        self.timeline = {"eras": [{"name": "Ancient Era", "events": []}]}
        self.calendar = {
            "months": ["Month 1", "Month 2", "Month 3", "Month 4"],
            "days_per_week": 7,
            "current_year": 1000
        }
        self.modules = {m: [] for m in mods}
        self.relations = []
        self.tags = []
        self.facts = []
        
        self.save()
        return self.current_id

    def load(self, proj_id: str):
        p_dir = os.path.join(self.base_path, proj_id)
        if not os.path.exists(p_dir): return False
        
        with open(os.path.join(p_dir, "config.json"), "r", encoding="utf-8") as f:
            self.config = json.load(f)
        with open(os.path.join(p_dir, "world.json"), "r", encoding="utf-8") as f:
            self.world = json.load(f)
        
        plot_path = os.path.join(p_dir, "story", "plot.json")
        if os.path.exists(plot_path):
            with open(plot_path, "r", encoding="utf-8") as f:
                self.plot = json.load(f)
        
        timeline_path = os.path.join(p_dir, "lore", "timeline.json")
        if os.path.exists(timeline_path):
            with open(timeline_path, "r", encoding="utf-8") as f:
                self.timeline = json.load(f)

        cal_path = os.path.join(p_dir, "lore", "calendar.json")
        if os.path.exists(cal_path):
            with open(cal_path, "r", encoding="utf-8") as f:
                self.calendar = json.load(f)

        rv_path = os.path.join(p_dir, ".nexus", "recently_viewed.json")
        if os.path.exists(rv_path):
            with open(rv_path, "r", encoding="utf-8") as f:
                self.recently_viewed = json.load(f)

        facts_path = os.path.join(p_dir, "lore", "facts.json")
        if os.path.exists(facts_path):
            with open(facts_path, "r", encoding="utf-8") as f:
                self.facts = json.load(f)
        
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
            (os.path.join("story", "plot.json"), self.plot),
            (os.path.join("lore", "timeline.json"), self.timeline),
            (os.path.join("lore", "calendar.json"), self.calendar),
            (os.path.join(".nexus", "recently_viewed.json"), self.recently_viewed),
            (os.path.join("lore", "facts.json"), self.facts)
        ]
        
        for filename, data in files:
            with open(os.path.join(p_dir, filename), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        for mod, data in self.modules.items():
            path = os.path.join(p_dir, "modules", f"{mod}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    def create_snapshot(self, label: str):
        if not self.current_id: return
        snap_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snap_dir = os.path.join(self.get_dir(), "snapshots", snap_id)
        os.makedirs(snap_dir)
        
        data = {
            "label": label,
            "timestamp": datetime.now().isoformat(),
            "world": self.world,
            "config": self.config,
            "modules": self.modules,
            "plot": self.plot,
            "timeline": self.timeline,
            "facts": self.facts
        }
        with open(os.path.join(snap_dir, "data.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return snap_id
