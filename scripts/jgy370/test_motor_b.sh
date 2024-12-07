#!/bin/bash

# Setup GPIO modes for TB6612FNG
gpio -g mode 18 pwm  # PWMB
gpio -g mode 13 out  # BIN1
gpio -g mode 19 out  # BIN2
gpio -g mode 1 out   # STBY

# Disable standby
gpio -g write 1 1

# Set motor B direction to forward
gpio -g write 13 1  # BIN1
gpio -g write 19 0  # BIN2

# Set PWM duty cycle for speed control (0-1023)
gpio -g pwm 18 512  # PWMB (Motor B speed)

# Print the GPIO pin states for debugging
gpio readall
