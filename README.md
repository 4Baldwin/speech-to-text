# Speech to Text (Thai)

แอปพลิเคชันเดสก์ท็อปสำหรับแปลงเสียงพูดภาษาไทยเป็นข้อความ  
รองรับทั้งไฟล์เสียง และการรับเสียงจากไมโครโฟนแบบ Start/Stop  
สร้างด้วย Python, Flet, SpeechRecognition และ PyAudio

---

## คุณสมบัติ (Features)

### รองรับการแปลงเสียง 2 รูปแบบ

1) แปลงไฟล์เสียงเป็นข้อความ
- รองรับไฟล์: .mp3, .wav, .m4a, .flac
- แสดงชื่อไฟล์ที่เลือก
- ประมวลผลผ่าน Google Speech Recognition

2) รับเสียงจากไมโครโฟน
- ปุ่ม Start / Stop Recording
- บันทึกเสียงไมค์แบบเรียลไทม์
- แปลงเสียงเป็นข้อความเมื่อกดหยุด

---

## ส่วนติดต่อผู้ใช้ (UI)
- ปุ่มเลือกไฟล์เสียง
- ปุ่มเริ่ม/หยุดรับเสียงจากไมโครโฟน
- แถบสถานะการทำงาน
- แสดงชื่อไฟล์ที่กำลังใช้งาน
- กล่องผลลัพธ์ข้อความ (อ่านอย่างเดียว)
- Footer แสดงชื่อผู้พัฒนา

---

## เทคโนโลยีที่ใช้ (Tech Stack)

| ส่วน | เทคโนโลยี |
|------|-----------|
| GUI Framework | Flet |
| Speech-to-Text Engine | Google Speech Recognition API |
| Audio Recording | PyAudio |
| Audio Processing | Pydub + FFmpeg |
| Python | Portable Python 3.12 |

---

## โครงสร้างโปรเจกต์ (Project Structure)
```
speech-to-text/
├── app/
│ ├── gui.py
│ ├── stt_service.py
│ ├── config.py
│ └── init.py
│
├── ffmpeg/
│ └── bin/
│ ├── ffmpeg.exe
│ ├── ffplay.exe
│ └── ffprobe.exe
│
├── python/
│ └── python.exe
│
├── main.py
├── requirements.txt
└── Run_speech_to_text.bat
```
---

## วิธีติดตั้ง (Installation)

1. เตรียมโครงสร้างโปรเจกต์ให้ตรงกับด้านบน  
2. ติดตั้ง dependencies (ใช้ Python portable):
- python\python.exe -m pip install -r requirements.txt --prefix python
4. รันโปรแกรม:
- python\pythonw.exe main.py
   
หรือใช้ไฟล์: 
- Run_speech_to_text.bat
ซึ่งมีระบบตรวจสอบ dependencies + FFmpeg + splash screen

---

## วิธีใช้งาน (Usage)

### แปลงไฟล์เสียงเป็นข้อความ
1. กดปุ่ม "เลือกไฟล์เสียง"
2. เลือกไฟล์เสียงที่ต้องการ
3. รอประมวลผล
4. ข้อความจะปรากฏในช่องผลลัพธ์

### รับเสียงจากไมค์
1. กดปุ่ม "Start Recording"
2. พูดใส่ไมโครโฟน
3. กด "Stop Recording"
4. ระบบจะแปลงเสียงเป็นข้อความทันที

---

## ข้อกำหนดระบบ (Requirements)
- Windows 10 หรือ Windows 11
- ไมโครโฟน (สำหรับโหมดไมค์)
- อินเทอร์เน็ต (ใช้ Google Speech Recognition)

---

## ผู้พัฒนา
Supawat Arrakrattakun
