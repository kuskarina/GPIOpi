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
    duty = 2 + (angle / 18)  # Convert angle to duty cycle (2-12 range)
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Allow the servo to move
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    # Step 1: Move to 0° (baseline)
    print("Moving to 0°")
    set_servo_angle(0)
    time.sleep(1)

    # Step 2: Walk through angles in 15° increments
    for angle in range(0, 181, 15):  # 0° to 180° in steps of 15
        print(f"Moving to {angle}°")
        set_servo_angle(angle)
        time.sleep(1)

    # Step 3: Walk back to 0° in 15° increments
    for angle in range(180, -1, -15):  # 180° to 0° in steps of -15
        print(f"Moving to {angle}°")
        set_servo_angle(angle)
        time.sleep(1)

    print("Servo test complete.")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
