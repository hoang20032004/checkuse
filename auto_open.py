import subprocess
import os
import sys

def get_connected_devices(adb_path):
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Bỏ dòng đầu
        devices = []

        for line in lines:
            if line.strip() and "device" in line:
                serial = line.split("\t")[0]
                devices.append(serial)

        return devices
    except FileNotFoundError:
        print("❌ Không tìm thấy adb.exe.")
        return []

def open_youtube_all_devices(adb_path):
    devices = get_connected_devices(adb_path)
    if not devices:
        print("⚠️ Không có thiết bị nào đang kết nối.")
        return

    print(f"🔍 Đã phát hiện {len(devices)} thiết bị. Đang gửi lệnh mở YouTube...")
    for serial in devices:
        subprocess.run([adb_path, "-s", serial, "shell", "am", "start", "-a",
                        "android.intent.action.VIEW", "-d", "https://www.youtube.com/watch?v=EV-91JV4Fws"])
        print(f"✅ Đã gửi lệnh tới: {serial}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = os.path.join(base_dir,'platform-tools', 'platform-tools', 'adb.exe' )
    open_youtube_all_devices(adb_path)
    input("\nNhấn Enter để thoát...")
