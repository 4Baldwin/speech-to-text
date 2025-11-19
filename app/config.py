from pathlib import Path

# โฟลเดอร์ root ของโปรเจกต์ (speech-to-text)
BASE_DIR = Path(__file__).resolve().parent.parent

# โฟลเดอร์ assets (ถ้าอยากใช้รูปทีหลัง)
ASSETS_DIR = BASE_DIR / "assets"

# โฟลเดอร์เก็บไฟล์ชั่วคราว
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# ไฟล์ wav ชั่วคราว
TEMP_WAV_FILE = TEMP_DIR / "temp_audio.wav"

# ภาษา
LANGUAGE = "th-TH"
