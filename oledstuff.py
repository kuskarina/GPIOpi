import os
import psutil
import time
from PIL import Image, ImageDraw, ImageFont
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Function to get system stats
def get_system_stats():
    cpu_usage = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    ram_usage = ram.used / (1024 ** 2)  # Convert to MB
    ram_total = ram.total / (1024 ** 2)  # Convert to MB
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        cpu_temp = int(f.read()) / 1000  # Convert to Celsius
    return cpu_usage, cpu_temp, ram_usage, ram_total

# Clear the display
oled.fill(0)
oled.show()

# Load a larger font (TrueType font)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Path to font
large_font = ImageFont.truetype(font_path, 14)  # Font size 14
cat_font = ImageFont.truetype(font_path, 10)   # Larger font for the cat face

# Function to draw a larger cat face
def draw_cat_face(draw):
    draw.text((0, 0), " /\\_/\\", font=cat_font, fill=255)
    draw.text((0, 16), "( o.o )", font=cat_font, fill=255)
    draw.text((0, 32), " > ^ <", font=cat_font, fill=255)

# Main loop
while True:
    # Create a blank image for drawing
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Get system stats
    cpu_usage, cpu_temp, ram_usage, ram_total = get_system_stats()

    # Draw the cat face
    draw_cat_face(draw)

    # Add system stats to the right of the cat face
    draw.text((47, 0), f"CPU: {cpu_usage:.1f}%", font=large_font, fill=255)
    draw.text((47, 20), f"TEMP: {cpu_temp:.1f}C", font=large_font, fill=255)
    draw.text((47, 40), f"RAM: {ram_usage:.1f}/{ram_total:.1f}MB", font=large_font, fill=255)

    # Display the image
    oled.image(image)
    oled.show()

    # Wait a bit before refreshing
    time.sleep(1)

