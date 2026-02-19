import flet as ft
import json
import subprocess
import os

CONFIG_FILE = "config.json"
CORE_FILE = "v2ray"

process = None


# تحميل config
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return None


# حفظ config
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


# تشغيل V2Ray
def start_vpn(status_text):
    global process

    if process is None:

        if not os.path.exists(CONFIG_FILE):
            status_text.value = "config.json غير موجود"
            return

        try:
            process = subprocess.Popen(
                [CORE_FILE, "-config", CONFIG_FILE],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            status_text.value = "VPN متصل"
        except Exception as e:
            status_text.value = f"خطأ: {e}"


# إيقاف V2Ray
def stop_vpn(status_text):
    global process

    if process:
        process.terminate()
        process = None
        status_text.value = "VPN غير متصل"


# واجهة التطبيق
def main(page: ft.Page):

    page.title = "My V2Ray VPN"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text(
        "V2Ray VPN",
        size=32,
        weight="bold"
    )

    status = ft.Text(
        "VPN غير متصل",
        size=20,
        color="red"
    )

    config_box = ft.TextField(
        label="V2Ray Config JSON",
        multiline=True,
        min_lines=10,
        max_lines=15,
        width=400
    )

    # تحميل config إلى textbox
    cfg = load_config()
    if cfg:
        config_box.value = json.dumps(cfg, indent=2)

    def connect(e):
        save_config(json.loads(config_box.value))
        start_vpn(status)
        status.color = "green"
        page.update()

    def disconnect(e):
        stop_vpn(status)
        status.color = "red"
        page.update()

    page.add(
        title,
        status,
        config_box,
        ft.Row(
            [
                ft.ElevatedButton("اتصال", on_click=connect),
                ft.ElevatedButton("قطع الاتصال", on_click=disconnect),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.app(target=main)
