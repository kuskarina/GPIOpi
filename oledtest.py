import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Initialize I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create SSD1306 OLED class
oled = SSD1306_I2C(128, 64, i2c)  # Adjust to (128, 32) if your screen is smaller

# Clear the display
oled.fill(0)
oled.show()

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Draw text
font = ImageFont.load_default()
draw.text((0, 0), "Hello, World!", font=font, fill=255)

# Display the image
oled.image(image)
oled.show()
