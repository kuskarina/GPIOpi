import time
import psutil
import requests
from datetime import datetime
from PIL import Image, ImageSequence, ImageDraw, ImageFont
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.fill(0)
oled.show()

# Open-Meteo API setup
LATITUDE = 35.2226  # Latitude for Norman, OK
LONGITUDE = -97.4395  # Longitude for Norman, OK
WEATHER_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"

# Load Kirby GIF
kirby_gif_path = "pikachu.gif"  # Replace with your Kirby GIF file path
kirby_gif = Image.open(kirby_gif_path)

# Load font for overlay text
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 14)  # Small font for overlay

# Function to fetch weather data
def fetch_weather():
    try:
        response = requests.get(WEATHER_URL)
        data = response.json()
        temp_celsius = data["current_weather"]["temperature"]
        temp_fahrenheit = (temp_celsius * 9 / 5) + 32
        return temp_fahrenheit
    except Exception as e:
        print("Error fetching weather:", e)
        return "N/A"

# Function to get CPU temperature
def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            cpu_temp = int(f.read()) / 1000  # Convert millidegree Celsius to Celsius
        return cpu_temp * 9 / 5 + 32  # Convert to Fahrenheit
    except:
        return "N/A"

# Main loop to display Kirby animation with overlay
try:
    while True:
        for frame in ImageSequence.Iterator(kirby_gif):
            # Resize and convert the GIF frame to fit the OLED
            frame = frame.resize((128, 64)).convert("1")  # Convert to 1-bit monochrome

            # Create an overlay for text
            draw = ImageDraw.Draw(frame)

            # Add system and weather info
            current_time = datetime.now().strftime("%I:%M:%S %p")
            weather_temp = fetch_weather()
            cpu_temp = get_cpu_temp()

            # Draw text at specified positions
            draw.text((2, 0), current_time, font=font, fill=0)  # Top of the screen
            draw.text((2, 35), f"CPU:  {cpu_temp:.1f}F", font=font, fill=0)  # Middle of the screen
            draw.text((2, 50), f"Norman: {weather_temp:.1f}F", font=font, fill=0)  # Bottom of the screen

            # Display the frame with overlay
            oled.image(frame)
            oled.show()

            # Small delay for animation speed
            time.sleep(0.1)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
