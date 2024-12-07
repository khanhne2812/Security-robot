#!/bin/bash

# Setup GPIO modes for TB6612FNG
gpio -g mode 12 pwm  # PWMA
gpio -g mode 5 out   # AIN1
gpio -g mode 6 out   # AIN2
gpio -g mode 1 out   # STBY

# Disable standby
gpio -g write 1 1

# Set motor A direction to forward
gpio -g write 5 1  # AIN1
gpio -g write 6 0  # AIN2

# Set PWM duty cycle for speed control (0-1023)
gpio -g pwm 12 700  # PWMA (Motor A speed)

# Print the GPIO pin states for debugging
gpio readall
