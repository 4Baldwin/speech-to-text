from app.stt_service import mic_to_text

if __name__ == "__main__":
    try:
        print("พูดได้เลย...")
        text = mic_to_text()
        print("ข้อความที่ได้:", text)
    except Exception as e:
        print("เกิดข้อผิดพลาด:", e)
