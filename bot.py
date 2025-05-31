# Görev dosyası yolu
import requests
import schedule
import time
from datetime import datetime, timedelta
import os

# OPENWEATHER AYARLARI
OPENWEATHER_API_KEY = 'f076dd6a64859cf92df0b1818fbb41d3'  # Buraya API anahtarını yaz
CITY = "Maltepe,TR"

# Görev dosyası yolu
TASK_FILE = "gorevler.txt"

def send_notification(title, message):
    # notify-send komutunu kullanarak sistem bildirimi gönderir
    os.system(f'notify-send "{title}" "{message}"')
    print(f"[{datetime.now().strftime('%H:%M')}] Bildirim gönderildi: {title}")

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
        response = requests.get(url).json()

        temp = response["main"]["temp"]
        wind = response["wind"]["speed"]
        desc = response["weather"][0]["description"]

        weather_message = f"📍 Maltepe Hava Durumu\n🌡 Sıcaklık: {temp}°C\n💨 Rüzgar: {wind} m/s\n🌤 Durum: {desc}"
        send_notification("Maltepe Hava Durumu", weather_message)

    except Exception as e:
        print(f"Hava durumu alınırken hata oluştu: {e}")

def check_tasks():
    now = datetime.now()
    target_time = (now + timedelta(minutes=30)).strftime("%H:%M")

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() == "":
                    continue
                time_str, task = line.strip().split(" ", 1)
                if time_str == target_time:
                    send_notification("⏰ Görev Hatırlatma", f"Yaklaşan Görevine Yarım Saat Kaldı ({time_str}):\n{task}")
    except FileNotFoundError:
        print("gorevler.txt dosyası bulunamadı.")

# Planlayıcılar
schedule.every(3).hours.at(":00").do(get_weather)
schedule.every(1).minutes.do(check_tasks)
get_weather()  # Başlangıçta hava durumunu al

print("Bot çalışıyor... Çıkmak için Ctrl+C")
while True:
    schedule.run_pending()
    time.sleep(1)
