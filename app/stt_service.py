import os
from pathlib import Path
import threading
import wave

import speech_recognition as sr
from pydub import AudioSegment
import pyaudio

from .config import TEMP_WAV_FILE, LANGUAGE, BASE_DIR

# ---------- FFmpeg สำหรับไฟล์เสียง ----------
FFMPEG_BIN = BASE_DIR / "ffmpeg" / "bin" / "ffmpeg.exe"

os.environ["PATH"] += os.pathsep + str(BASE_DIR / "ffmpeg" / "bin")
os.environ["FFMPEG_BINARY"] = str(FFMPEG_BIN)

AudioSegment.converter = str(FFMPEG_BIN)
print("FFMPEG PATH:", AudioSegment.converter)

# ---------- ตัวแปรสำหรับอัดเสียงจากไมค์ ----------
_CHUNK = 1024
_FORMAT = pyaudio.paInt16
_CHANNELS = 1
_RATE = 16000

_pa = None
_stream = None
_frames = []
_is_recording = False
_record_thread = None


def mp3_file_to_text(mp3_path: str) -> str:
    """
    แปลงไฟล์เสียง (mp3/wav/ฯลฯ ที่ pydub รองรับ) เป็นข้อความ
    """
    mp3_path = Path(mp3_path)

    sound = AudioSegment.from_file(mp3_path)
    sound.export(TEMP_WAV_FILE, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(str(TEMP_WAV_FILE)) as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data, language=LANGUAGE)
    return text


def _record_loop():
    global _frames, _is_recording, _stream
    while _is_recording:
        data = _stream.read(_CHUNK)
        _frames.append(data)


def start_mic_recording():
    """
    เริ่มอัดเสียงจากไมโครโฟน (กดปุ่มเริ่ม)
    """
    global _pa, _stream, _frames, _is_recording, _record_thread

    if _is_recording:
        return  # ถ้ากำลังอัดอยู่แล้วไม่ต้องทำอะไร

    _pa = pyaudio.PyAudio()
    _stream = _pa.open(
        format=_FORMAT,
        channels=_CHANNELS,
        rate=_RATE,
        input=True,
        frames_per_buffer=_CHUNK,
    )

    _frames = []
    _is_recording = True

    _record_thread = threading.Thread(target=_record_loop, daemon=True)
    _record_thread.start()


def stop_mic_and_get_text() -> str:
    """
    หยุดอัดเสียงจากไมค์, เซฟเป็นไฟล์ wav ชั่วคราว แล้วแปลงเป็นข้อความ
    """
    global _pa, _stream, _frames, _is_recording, _record_thread

    if not _is_recording:
        raise RuntimeError("ไมค์ยังไม่ได้เริ่มอัดเสียง")

    _is_recording = False
    if _record_thread and _record_thread.is_alive():
        _record_thread.join()

    # ปิด stream และ PyAudio
    _stream.stop_stream()
    _stream.close()
    _pa.terminate()

    # เซฟเป็น wav
    with wave.open(str(TEMP_WAV_FILE), "wb") as wf:
        wf.setnchannels(_CHANNELS)
        wf.setsampwidth(_pa.get_sample_size(_FORMAT))
        wf.setframerate(_RATE)
        wf.writeframes(b"".join(_frames))

    # ใช้ SpeechRecognition แปลงเสียงเป็นข้อความ
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(TEMP_WAV_FILE)) as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data, language=LANGUAGE)
    return text
