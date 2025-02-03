import RPi.GPIO as GPIO
import time

# Set up GPIO for servo
SERVO_PIN = 18  # GPIO pin connected to the servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM for servo
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz PWM frequency
pwm.start(0)  # Initialize with 0 duty cycle

def set_servo_angle(angle):
    """Sets the servo to a specific angle."""
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Allow the servo to move
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

def get_cpu_temp():
    """Reads the CPU temperature."""
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
        temp = temp_file.read()
    return float(temp) / 1000  # Convert to Celsius

def determine_servo_position(temp):
    """Determines servo angle based on temperature."""
    if temp < 45:  # Low temperature
        return 0
    elif 45 <= temp <= 70:  # Medium temperature
        return 90
    else:  # High temperature
        return 180

try:
    # Step 1: Initialize servo to 0° position
    print("Initializing to 0° position...")
    set_servo_angle(0)
    time.sleep(2)

    # Step 2: Start temperature monitoring
    while True:
        cpu_temp = get_cpu_temp()
        print(f"CPU Temperature: {cpu_temp:.2f}°C")

        # Determine servo position based on temperature
        angle = determine_servo_position(cpu_temp)
        print(f"Moving to {angle}° position.")
        set_servo_angle(angle)

        # Update every 1 second
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    pwm.stop()
    GPIO.cleanup()
