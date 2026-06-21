# bale -> @parsaeghbali
# address bot -> @python_learnbot

import os
import shutil

# مسیر پوشه‌ای که فایل‌ها داخل آن هستند
folder_path = r"C:\Users\re7\Downloads"

# دسته‌بندی پسوندها
file_types = {
    "PDF": [".pdf"],
    "Photo": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Documents": [".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Excel": [".xls", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
}

# ساخت دیکشنری برای جستجوی سریع
extension_map = {}
for category, extensions in file_types.items():
    for ext in extensions:
        extension_map[ext] = category

# بررسی فایل‌ها
for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)

    # فقط فایل‌ها
    if os.path.isfile(item_path):
        _, ext = os.path.splitext(item)
        ext = ext.lower()

        # تعیین پوشه مقصد
        category = extension_map.get(ext, "Others")

        destination_folder = os.path.join(folder_path, category)
        os.makedirs(destination_folder, exist_ok=True)

        # انتقال فایل
        shutil.move(item_path, os.path.join(destination_folder, item))

print("دسته‌بندی فایل‌ها با موفقیت انجام شد.")