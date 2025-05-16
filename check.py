import subprocess
import os
import sys
from datetime import datetime

def check_adb_devices(adb_path):
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Bỏ dòng đầu
        devices = []

        for line in lines:
            if line.strip() and "device" in line:
                serial = line.split("\t")[0]
                devices.append(serial)

        if not devices:
            print("⚠️ Không có thiết bị nào đang kết nối.")
        else:
            print("📱 Thiết bị đang kết nối:")
            for i, serial in enumerate(devices, 1):
                print(f"[{i}] {serial}")

    except FileNotFoundError:
        print("❌ Không tìm thấy adb.exe. Kiểm tra lại đường dẫn adb.")
        input("Nhấn Enter để thoát...")
        sys.exit(1)

def check_git_repository():
    return os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.git'))

def git_add_commit_push():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], cwd=base_dir, check=True)
        
        # Commit changes
        commit_msg = f"Update {os.path.basename(base_dir)} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=base_dir, check=True)
        
        # Push changes
        subprocess.run(['git', 'push'], cwd=base_dir, check=True)
        print("✅ Đã push lên Git thành công!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi push lên Git: {str(e)}")
        return False
    return True

if __name__ == "__main__":
    if not check_git_repository():
        print("❌ Thư mục hiện tại không phải là Git repository")
        input("Nhấn Enter để thoát...")
        sys.exit(1)
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    adb_path = os.path.join(base_dir, 'platform-tools', 'platform-tools', 'adb.exe')

    check_adb_devices(adb_path)
    git_add_commit_push()
    input("\nNhấn Enter để thoát...")
