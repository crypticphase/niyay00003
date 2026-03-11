# NEXUS GOD WRITER - Modular Version

โปรเจกต์นี้ถูกปรับโครงสร้างใหม่ให้เป็นระบบ Modular เพื่อความเป็นมืออาชีพและรองรับการขยายตัวในอนาคต

## โครงสร้างไฟล์ (File Structure)

- `main.py`: จุดเริ่มต้นของโปรแกรม
- `nexus/`: แพ็คเกจหลัก
    - `engine/`: ส่วนประมวลผล (Project Management, AI Connector)
    - `ui/`: ส่วนติดต่อผู้ใช้ (Main Window, Editor, Module Manager, AI Panel, Wiki)
- `projects/`: โฟลเดอร์เก็บข้อมูลนิยาย

## วิธีการรัน (How to Run)

1. ติดตั้งไลบรารี: `pip install -r requirements.txt`
2. ตั้งค่า API Key ในไฟล์ `.env`
3. รันโปรแกรม: `python main.py`

## ฟีเจอร์ที่อัปเกรด
- **Modular Architecture**: แยกส่วนการทำงานชัดเจน
- **Advanced AI Context**: ระบบ AI ที่ฉลาดขึ้นและเข้าใจบริบทโลกได้ดีขึ้น
- **Rich Text Editor**: ระบบเขียนนิยายพร้อมสถิติและ Auto-save
- **Lore Wiki**: ระบบค้นหาข้อมูลโลกแบบรวมศูนย์
- **Consistency Checker**: ระบบ AI ตรวจสอบความสมเหตุสมผลของเนื้อเรื่อง
