# bale -> @parsaeghbali
# address bot -> @python_learnbot
# https://github.com/r-eghbali7/13-challenge_python.git

import requests
from datetime import datetime

API_KEY = "b2021bd85ac5f998ba1987581dc45ced"

def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=fa"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "time": datetime.fromtimestamp(data["dt"])
        }

        return weather

    except requests.exceptions.RequestException:
        return None


def show_weather(info):
    print("\n" + "=" * 40)
    print(f"📍 شهر: {info['city']} ({info['country']})")
    print(f"🌡 دما: {info['temp']}°C")
    print(f"🤔 دمای محسوس: {info['feels_like']}°C")
    print(f"💧 رطوبت: {info['humidity']}%")
    print(f"🌪 سرعت باد: {info['wind_speed']} m/s")
    print(f"📊 فشار هوا: {info['pressure']} hPa")
    print(f"☁ وضعیت: {info['description']}")
    print(f"🕒 بروزرسانی: {info['time']}")
    print("=" * 40)


def main():
    city = input("نام شهر را وارد کنید: ")

    weather = get_weather(city)

    if weather:
        show_weather(weather)
    else:
        print("❌ خطا در دریافت اطلاعات یا نام شهر اشتباه است.")


if __name__ == "__main__":
    main()