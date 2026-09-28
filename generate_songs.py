"""
Funk Land - ساخت خودکار songs.json با کاور
"""
import os
import json
import time

# ==================== تنظیمات ====================
UPLOADS_DIR = "uploads"
COVERS_DIR = "covers"
OUTPUT_FILE = "songs.json"
AUDIO_EXT = [".mp3", ".m4a", ".ogg", ".wav", ".webm", ".flac", ".aac", ".opus"]
IMAGE_EXT = [".jpg", ".jpeg", ".png", ".webp", ".gif"]

# ==================== خوندن songs.json قبلی ====================
existing = {}
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            for song in json.load(f):
                existing[song["file"]] = song
    except Exception as e:
        print(f"خطا در خوندن songs.json: {e}")

# ==================== پیدا کردن کاورها ====================
covers = {}
if os.path.exists(COVERS_DIR):
    for filename in os.listdir(COVERS_DIR):
        if any(filename.lower().endswith(ext) for ext in IMAGE_EXT):
            # اسم بدون پسوند
            base = os.path.splitext(filename)[0].lower()
            covers[base] = filename

print(f"🖼️ {len(covers)} کاور پیدا شد")

# ==================== پیدا کردن فایل‌های صوتی ====================
if not os.path.exists(UPLOADS_DIR):
    print(f"پوشه {UPLOADS_DIR} وجود نداره!")
    exit(1)

songs = []
files = sorted(os.listdir(UPLOADS_DIR))

for filename in files:
    if not any(filename.lower().endswith(ext) for ext in AUDIO_EXT):
        continue
    
    filepath = os.path.join(UPLOADS_DIR, filename)
    if not os.path.isfile(filepath):
        continue
    
    # اسم پایه (بدون پسوند صوتی)
    base = os.path.splitext(filename)[0].lower()
    
    # پیدا کردن کاور (با اسم مشابه)
    cover_file = ""
    if base in covers:
        cover_file = covers[base]
    else:
        # تلاش برای پیدا کردن کاور با اسم‌های مشابه
        # مثلاً: "no-era-amor-super-slowed" → "no-era-amor"
        for cover_base, cover_name in covers.items():
            if base.startswith(cover_base) or cover_base in base:
                cover_file = cover_name
                break
    
    if filename in existing:
        song = existing[filename]
        # اگه کاور جدید پیدا شد، آپدیت کن
        if cover_file and song.get("cover") != cover_file:
            song["cover"] = cover_file
            print(f"🖼️ کاور جدید برای: {filename}")
        print(f"✅ قدیمی: {filename} → {song['name']}")
    else:
        # اسم نمایشی
        name = base.replace("-", " ").replace("_", " ")
        name = " ".join(name.split())
        name = name.title()
        
        song = {
            "name": name,
            "file": filename,
            "cover": cover_file,
            "date": int(time.time())
        }
        if cover_file:
            print(f"🆕 جدید + کاور: {filename}")
        else:
            print(f"🆕 جدید (بدون کاور): {filename}")
    
    songs.append(song)

# ==================== مرتب‌سازی ====================
songs.sort(key=lambda x: x.get("date", 0), reverse=True)

# ==================== نوشتن ====================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)

print(f"\n✅ songs.json ساخته شد — {len(songs)} آهنگ")
