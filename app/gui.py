import flet as ft
from .stt_service import (
    mp3_file_to_text,
    start_mic_recording,
    stop_mic_and_get_text,
)


def main(page: ft.Page):
    page.title = "Speech to Text (Thai)"
    page.theme_mode = ft.ThemeMode.DARK

    # ---------------- Header ----------------
    title = ft.Text(
        "🎙️ Speech to Text (Thai)",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    # ---------------- Status Bar ----------------
    status_text = ft.Text(
        "🟢 พร้อมใช้งาน",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_400,
    )

    file_name_text = ft.Text(
        "ยังไม่ได้เลือกไฟล์เสียง",
        size=16,
        color=ft.Colors.GREY_400,
        italic=True,
    )

    def set_status(status: str):
        status_map = {
            "idle": ("🟢 พร้อมใช้งาน", ft.Colors.GREEN_400),
            "listening": ("🔵 กำลังบันทึกเสียงจากไมค์...", ft.Colors.BLUE_400),
            "processing_file": ("🟡 กำลังแปลงไฟล์เสียง...", ft.Colors.AMBER_300),
            "processing_mic": ("🟣 กำลังแปลงเสียงจากไมค์...", ft.Colors.PURPLE_300),
            "error": ("🔴 มีข้อผิดพลาด", ft.Colors.RED_400),
        }

        text, color = status_map.get(status, ("", ft.Colors.GREY_400))
        status_text.value = text
        status_text.color = color
        page.update()

    # ---------------- Output ----------------
    output_label = ft.Text(
        "ช่องแสดงผลลัพธ์ข้อความ",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREY_300,
        text_align=ft.TextAlign.CENTER,
    )

    output_field = ft.TextField(
        multiline=True,
        min_lines=10,
        read_only=True,
        border_radius=10,
        filled=True,
        border=ft.border.all(1, ft.Colors.GREY_700),
        border_color=ft.Colors.GREY_700,
        hint_text="ยังไม่ได้รับข้อความใด ๆ",
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
    )

    # ---------------- File Picker ----------------
    def on_file_result(e: ft.FilePickerResultEvent):
        if not e.files:
            set_status("error")
            status_text.value = "🔴 ยังไม่ได้เลือกไฟล์เสียง"
            file_name_text.value = "ยังไม่ได้เลือกไฟล์เสียง"
            page.update()
            return

        file = e.files[0]
        file_name_text.value = f"ไฟล์ที่เลือก: {file.name}"
        set_status("processing_file")
        output_field.value = ""
        page.update()

        try:
            text = mp3_file_to_text(file.path)
            output_field.value = text
            set_status("idle")
        except Exception as ex:
            set_status("error")
            status_text.value = f"🔴 ข้อผิดพลาดในการแปลงไฟล์: {ex}"
        finally:
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)

    def select_file_click(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["mp3", "wav", "m4a", "flac"],
        )

    select_file_button = ft.ElevatedButton(
        "เลือกไฟล์เสียง",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=select_file_click,
    )

    # ---------------- Mic Button (Start/Stop) ----------------
    is_recording = {"value": False}

    def mic_click(e):
        if not is_recording["value"]:
            try:
                start_mic_recording()
                is_recording["value"] = True
                set_status("listening")
                file_name_text.value = "กำลังบันทึกเสียงจากไมค์..."
                output_field.value = ""
                mic_button.text = "หยุดรับเสียงจากไมค์"
                mic_button.icon = ft.Icons.STOP
                page.update()
            except Exception as ex:
                set_status("error")
                status_text.value = f"🔴 ไม่สามารถเริ่มอัดเสียงได้: {ex}"
                page.update()
        else:
            try:
                set_status("processing_mic")
                file_name_text.value = "กำลังแปลงเสียงจากไมค์..."
                page.update()

                text = stop_mic_and_get_text()
                output_field.value = text
                set_status("idle")
                file_name_text.value = "เสียงจากไมค์ (ไม่มีไฟล์)"
            except Exception as ex:
                set_status("error")
                status_text.value = f"🔴 ข้อผิดพลาดจากไมค์: {ex}"
            finally:
                is_recording["value"] = False
                mic_button.text = "เริ่มรับเสียงจากไมค์"
                mic_button.icon = ft.Icons.MIC
                page.update()

    mic_button = ft.ElevatedButton(
        "เริ่มรับเสียงจากไมค์",
        icon=ft.Icons.MIC,
        on_click=mic_click,
    )

    # ---------------- Footer ----------------
    footer = ft.Text(
        "By Supawat Arrakrattakun",
        size=16,
        color=ft.Colors.GREY_600,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    # ---------------- Layout ----------------
    page.add(
        ft.Column(
            [
                title,
                ft.Divider(),
                ft.Row(
                    [select_file_button, mic_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Divider(),
                status_text,
                file_name_text,
                output_label,
                output_field,
                ft.Divider(),
                footer,  # ⬅️ ย้ายมาล่างสุด
            ],
            spacing=12,
            expand=True,
        )
    )


def run_app():
    ft.app(target=main, view=ft.AppView.FLET_APP)
