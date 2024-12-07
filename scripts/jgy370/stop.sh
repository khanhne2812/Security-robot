#!/bin/bash

# Using WiringPi library
# Make sure WiringPi is installed: sudo apt-get install wiringpi

# Setup GPIO modes for TB6612FNG
# PWMA = GPIO 12 (WiringPi pin 26)
# PWMB = GPIO 13 (WiringPi pin 1)
# STBY = GPIO 1 (WiringPi pin 31)

# Set GPIO pins to WiringPi mode
gpio -g mode 12 pwm  # PWMA
gpio -g mode 13 pwm  # PWMB
gpio -g mode 1 out   # STBY

# Stop motors by setting PWM duty cycle to 0
gpio -g pwm 12 0  # PWMA
gpio -g pwm 13 0  # PWMB

# Enable standby mode
gpio -g write 1 0

# Cleanup GPIO (optional, useful for resetting pin states)
gpio -g mode 12 in
gpio -g mode 18 in
gpio -g mode 1 in

