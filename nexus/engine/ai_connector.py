import os
import requests
import json
from typing import Dict, List, Any

class AIConnector:
    """The Ultimate AI Connector for Nexus God Writer using Grok (xAI)."""
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.api_url = "https://api.x.ai/v1/chat/completions"
        self.model_name = "grok-beta" # คุณสามารถเปลี่ยนเป็น grok-2 ได้ถ้าต้องการ

    def ask(self, prompt: str, context: str):
        if not self.api_key: 
            return "ข้อผิดพลาด: ไม่พบ XAI_API_KEY ในระบบ กรุณาตั้งค่า Environment Variable"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_instruction = f"""คุณคือ NEXUS GOD WRITER ผู้ช่วยนักเขียนนิยายและนักสร้างโลกมืออาชีพ 
ใช้บริบทของโลก (Context) ต่อไปนี้เพื่อช่วยเหลือผู้เขียน จงมีความคิดสร้างสรรค์ รักษาความสมเหตุสมผล และให้รายละเอียดที่ลึกซึ้ง

บริบทของโลก:
{context}"""

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Grok API Error ({response.status_code}): {response.text}"
        except Exception as e:
            return f"AI Connection Error: {str(e)}"

    def check_consistency(self, context: str):
        prompt = "Analyze the entire world lore and story for any contradictions, plot holes, or character inconsistencies. Provide a detailed report."
        return self.ask(prompt, context)

    def analyze_story_director(self, story_content: str, context: str):
        prompt = f"""
        วิเคราะห์เนื้อเรื่องต่อไปนี้ในด้าน:
        1. ความขัดแย้ง (Conflict): รุนแรงพอไหม?
        2. จังหวะเรื่อง (Pacing): เร็วหรือช้าไปไหม?
        3. ความตึงเครียด (Tension): กราฟอารมณ์เป็นอย่างไร?
        4. การพัฒนาตัวละคร (Character Arc): ตัวละครมีการเปลี่ยนแปลงไหม?
        5. โครงสร้าง 3 องก์: ตอนนี้เราอยู่จุดไหนของเรื่อง?
        
        เนื้อเรื่อง:
        {story_content}
        """
        return self.ask(prompt, context)

    def continue_story(self, current_text: str, context: str):
        prompt = f"เขียนเนื้อเรื่องต่อจากข้อความนี้ โดยรักษาโทนและอารมณ์เดิม:\n\n{current_text}"
        return self.ask(prompt, context)

    def rewrite_story(self, selected_text: str, instruction: str, context: str):
        prompt = f"เกลาข้อความต่อไปนี้ตามคำสั่ง: '{instruction}'\n\nข้อความเดิม: {selected_text}"
        return self.ask(prompt, context)

    def expand_story(self, short_text: str, context: str):
        prompt = f"ขยายความเนื้อเรื่องส่วนนี้ให้เห็นภาพและอารมณ์ชัดเจนขึ้น:\n\n{short_text}"
        return self.ask(prompt, context)

    def generate_names(self, category: str, style: str, context: str):
        prompt = f"ช่วยคิดชื่อ {category} ในสไตล์ {style} มาให้หน่อยสัก 10 ชื่อที่เข้ากับโลกนี้"
        return self.ask(prompt, context)

    def get_worldbuilding_questions(self, context: str):
        prompt = "ช่วยถามคำถามชวนคิด 5 ข้อเพื่อช่วยขยายรายละเอียดของโลกนี้ (เช่น ระบบเวทมนตร์, การเมือง, วัฒนธรรม)"
        return self.ask(prompt, context)

    def summarize_lore(self, context: str):
        prompt = "สรุปข้อมูล Lore ทั้งหมดของโลกนี้เป็นย่อหน้าสั้นๆ สำหรับการ Pitch หรือแนะนำเรื่อง"
        return self.ask(prompt, context)

    def generate_lore(self, mod_type: str, schema: List[str], context: str):
        schema_str = ", ".join(schema)
        prompt = f"สร้างข้อมูล {mod_type} ที่ละเอียดและเข้ากับโลกนี้ โดยให้มีฟิลด์ดังนี้: {schema_str}"
        return self.ask(prompt, context)
