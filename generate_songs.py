"""
Funk Land - ساخت خودکار songs.json
همه آهنگ‌ها کاور پیش‌فرض FUNKLAND-lightlogo.pmg.png می‌گیرن
"""
import os
import json
import time

# ==================== تنظیمات ====================
UPLOADS_DIR = "uploads"
OUTPUT_FILE = "songs.json"

# ⚠️ اسم دقیق کاور پیش‌فرض
DEFAULT_COVER = "FUNKLAND-lightlogo.pmg.png"

AUDIO_EXT = [".mp3", ".m4a", ".ogg", ".wav", ".webm", ".flac", ".aac", ".opus"]

# ==================== خوندن songs.json قبلی ====================
existing = {}
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            for song in json.load(f):
                existing[song["file"]] = song
    except Exception as e:
        print(f"⚠️ خطا در خوندن songs.json: {e}")

# ==================== پیدا کردن فایل‌های صوتی ====================
if not os.path.exists(UPLOADS_DIR):
    print(f"❌ پوشه {UPLOADS_DIR} وجود نداره!")
    exit(1)

songs = []
files = sorted(os.listdir(UPLOADS_DIR))

print(f"\n🎵 پیدا کردن آهنگ‌ها از {UPLOADS_DIR}/\n")

for filename in files:
    if not any(filename.lower().endswith(ext) for ext in AUDIO_EXT):
        continue
    
    filepath = os.path.join(UPLOADS_DIR, filename)
    if not os.path.isfile(filepath):
        continue
    
    base = os.path.splitext(filename)[0].lower()
    
    if filename in existing:
        song = existing[filename]
        # همیشه کاور پیش‌فرض
        song["cover"] = DEFAULT_COVER
        print(f"✅ {filename} → {song['name']}")
    else:
        # اسم نمایشی
        name = base.replace("-", " ").replace("_", " ")
        name = " ".join(name.split())
        name = name.title()
        
        song = {
            "name": name,
            "file": filename,
            "cover": DEFAULT_COVER,
            "date": int(time.time())
        }
        print(f"🆕 {filename} → {name}")
    
    songs.append(song)

# ==================== مرتب‌سازی ====================
songs.sort(key=lambda x: x.get("date", 0), reverse=True)

# ==================== اطمینان از فیلدها ====================
for s in songs:
    s["cover"] = DEFAULT_COVER
    s.setdefault("date", 0)

# ==================== نوشتن ====================
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)

print(f"\n✅ songs.json ساخته شد — {len(songs)} آهنگ")
print(f"🖼️ همه با کاور پیش‌فرض: {DEFAULT_COVER}")
