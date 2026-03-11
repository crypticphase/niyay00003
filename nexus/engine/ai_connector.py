import os
import google.generativeai as genai
from typing import Dict, List, Any

class AIConnector:
    """The Ultimate AI Connector for Nexus God Writer."""
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3.1-pro-preview')
        else:
            self.model = None

    def ask(self, prompt: str, context: str):
        if not self.model: return "Error: Gemini API Key not found."
        
        full_prompt = f"""
        System: You are NEXUS GOD WRITER, a professional worldbuilding and story assistant.
        Use the following world context to help the writer. Be creative, consistent, and detailed.
        
        Context:
        {context}
        
        User Request:
        {prompt}
        """
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)}"

    def check_consistency(self, context: str):
        prompt = "Analyze the entire world lore and story for any contradictions, plot holes, or character inconsistencies. Provide a detailed report."
        return self.ask(prompt, context)

    def analyze_story_director(self, story_content: str, context: str):
        prompt = f"""
        Analyze the following story content for:
        1. Conflict: Is it strong enough?
        2. Pacing: Is it too fast or slow?
        3. Tension: How is the emotional curve?
        4. Character Arc: Are the characters developing?
        5. Three-Act Structure: Where are we in the story?
        
        Story Content:
        {story_content}
        """
        return self.ask(prompt, context)

    def generate_lore(self, mod_type: str, schema: List[str], context: str):
        schema_str = ", ".join(schema)
        prompt = f"Generate a detailed {mod_type} entry that fits perfectly into this world. Return in format: {schema_str}"
        return self.ask(prompt, context)
