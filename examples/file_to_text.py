from app.stt_service import mp3_file_to_text

if __name__ == "__main__":
    path = input("กรุณาใส่ path ของไฟล์เสียง: ")
    try:
        text = mp3_file_to_text(path)
        print("ข้อความที่ได้:", text)
    except Exception as e:
        print("เกิดข้อผิดพลาด:", e)
