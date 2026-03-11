import os
import json
from typing import List, Dict, Any

class SearchEngine:
    def __init__(self, engine):
        self.engine = engine

    def search(self, query: str) -> List[Dict[str, Any]]:
        if not self.engine.current_id:
            return []
        
        query = query.lower()
        results = []
        p_dir = self.engine.get_dir()

        # 1. Search Modules (Characters, Locations, etc.)
        for mod_name, items in self.engine.modules.items():
            for item in items:
                item_name = item.get("name", "")
                item_desc = str(item).lower()
                if query in item_name.lower() or query in item_desc:
                    results.append({
                        "type": "module",
                        "category": mod_name.replace("_", " ").capitalize(),
                        "title": item_name,
                        "snippet": self._get_snippet(str(item), query),
                        "data": mod_name
                    })

        # 2. Search Story Chapters
        story_dir = os.path.join(p_dir, "story")
        if os.path.exists(story_dir):
            for filename in sorted(os.listdir(story_dir)):
                if filename.endswith(".txt"):
                    path = os.path.join(story_dir, filename)
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if query in content.lower():
                            results.append({
                                "type": "story",
                                "category": "Story Chapter",
                                "title": filename.replace(".txt", ""),
                                "snippet": self._get_snippet(content, query),
                                "data": filename
                            })

        # 3. Search Lore Wiki
        # Assuming wiki data is stored in a way we can search. 
        # For now, let's search the world config and facts.
        world_str = str(self.engine.world).lower()
        if query in world_str:
            results.append({
                "type": "lore",
                "category": "World Config",
                "title": "World Settings",
                "snippet": self._get_snippet(world_str, query),
                "data": "world"
            })

        for fact in self.engine.facts:
            content = fact.get("content", "").lower()
            if query in content:
                results.append({
                    "type": "fact",
                    "category": "Quick Capture / Fact",
                    "title": "Fact Entry",
                    "snippet": self._get_snippet(content, query),
                    "data": fact
                })

        # 4. Search Timeline
        for era in self.engine.timeline.get("eras", []):
            for event in era.get("events", []):
                event_str = str(event).lower()
                if query in event_str:
                    results.append({
                        "type": "timeline",
                        "category": "Timeline",
                        "title": event.get("title", "Event"),
                        "snippet": self._get_snippet(event_str, query),
                        "data": era["name"]
                    })

        return results

    def _get_snippet(self, text: str, query: str, length: int = 100) -> str:
        idx = text.lower().find(query)
        if idx == -1:
            return text[:length] + "..."
        
        start = max(0, idx - length // 2)
        end = min(len(text), idx + length // 2)
        snippet = text[start:end].replace("\n", " ")
        if start > 0: snippet = "..." + snippet
        if end < len(text): snippet = snippet + "..."
        return snippet
