import time
from PIL import Image, ImageSequence
import board
import busio
from adafruit_ssd1306 import SSD1306_I2C

# Initialize I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.fill(0)
oled.show()

# Load the GIF
gif_path = "win98.gif"
gif = Image.open(gif_path)

# Main loop to play the GIF
try:
    while True:
        for frame in ImageSequence.Iterator(gif):
            # Clear the display to avoid artifacts
            oled.fill(0)
            
            # Resize and convert the frame to fit the OLED
            frame = frame.resize((128, 64)).convert("1")  # Convert to 1-bit monochrome
            
            # Display the frame
            oled.image(frame)
            oled.show()
            
            # Small delay for animation speed
            time.sleep(0.1)  # Adjust for smoother playback
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
