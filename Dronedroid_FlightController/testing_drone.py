import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM) # could also do GPIO.BOARD if using physical pin numbers
GPIO.setwarnings(False)

# Define pins for L293D motor driver
IN1 = 19  # Input 1
# IN2 = 27  # Input 2
EN = 26 #  Enable (PWM pin)

# Setup pins as output
GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# Create PWM object (frequency: 1000 Hz)
pwm = GPIO.PWM(EN, 1000)
pwm.start(0)  # Start with 0% duty cycle


def motor_forward(speed):
    """Run motor forward at given speed (0-100)"""
    GPIO.output(IN1, GPIO.HIGH)
    # GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def motor_backward(speed):
    """Run motor backward at given speed (0-100)"""
    GPIO.output(IN1, GPIO.LOW)
    # GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def motor_stop():
    """Stop the motor"""
    pwm.ChangeDutyCycle(0)

try:
    # Example: Run motor forward at 75% speed for 2 seconds
    motor_forward(100)
    time.sleep(2)
    
    motor_forward(75)
    time.sleep(2)
    
    # Run backward at 50% speed for 2 seconds
    motor_forward(50)
    time.sleep(2)

    motor_forward(20)
    time.sleep(2)
    
    # Stop motor
    motor_stop()
    
finally:
    pwm.stop()
    GPIO.cleanup()

