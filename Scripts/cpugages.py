import psutil
import time
from RPLCD.i2c import CharLCD

# Configure the I2C LCD
I2C_ADDR = 0x27  # Replace with your I2C address
lcd = CharLCD('PCF8574', I2C_ADDR, cols=16, rows=2)

def get_cpu_usage():
    """Returns the CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    """Returns the RAM usage percentage."""
    memory = psutil.virtual_memory()
    return memory.percent

def get_cpu_temp():
    """Reads the CPU temperature."""
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
        temp = temp_file.read()
    return float(temp) / 1000  # Convert to Celsius

def display_info():
    """Cycles through CPU usage, RAM usage, and CPU temperature."""
    while True:
        # CPU Usage
        lcd.clear()
        cpu_usage = get_cpu_usage()
        lcd.write_string(f"CPU Usage:\n{cpu_usage:.2f}%")
        time.sleep(2)

        # RAM Usage
        lcd.clear()
        ram_usage = get_ram_usage()
        lcd.write_string(f"RAM Usage:\n{ram_usage:.2f}%")
        time.sleep(2)

        # CPU Temperature
        lcd.clear()
        cpu_temp = get_cpu_temp()
        lcd.write_string(f"CPU Temp:\n{cpu_temp:.2f} C")
        time.sleep(2)

try:
    display_info()
except KeyboardInterrupt:
    # Clean up and clear the LCD
    lcd.clear()
    lcd.write_string("Goodbye!")
    time.sleep(2)
    lcd.clear()
