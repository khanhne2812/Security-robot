#!/bin/bash

# Using WiringPi library
# Make sure WiringPi is installed: sudo apt-get install wiringpi

# Setup GPIO modes for TB6612FNG
# PWMA = GPIO 12 (WiringPi pin 26)
# AIN1 = GPIO 5 (WiringPi pin 21)
# AIN2 = GPIO 6 (WiringPi pin 22)
# PWMB = GPIO 13 (WiringPi pin 1)
# BIN1 = GPIO 19 (WiringPi pin 23)
# BIN2 = GPIO 26 (WiringPi pin 24)
# STBY = GPIO 1 (WiringPi pin 31)

# Set GPIO pins to WiringPi mode
gpio -g mode 12 pwm  # PWMA
gpio -g mode 5 out   # AIN1
gpio -g mode 6 out   # AIN2
gpio -g mode 13 pwm  # PWMB
gpio -g mode 19 out  # BIN1
gpio -g mode 26 out  # BIN2
gpio -g mode 1 out   # STBY

# Disable standby
gpio -g write 1 1

# Set motor directions
# Forward direction for Motor A
gpio -g write 5 0  # AIN1
gpio -g write 6 1  # AIN2

# Forward direction for Motor B
gpio -g write 19 0  # BIN1
gpio -g write 26 1  # BIN2


# Set PWM duty cycle for speed control (0-1023)
# Example: 50% duty cycle (512/1023)
gpio -g pwm 12 468  # PWMA (Motor A speed)
gpio -g pwm 13 512  # PWMB (Motor B speed)

# Debugging output
echo "Motor A (GPIO 12) speed set to 512"
echo "Motor B (GPIO 13) speed set to 512"

