import pigpio

# Set servo pulse widths (in microseconds)
CENTER_PULSE = 1000
MAX_PULSE = 2500
MIN_PULSE = 500

# Initialize pigpio daemon
pi = pigpio.pi()

def set_servo_angle(pin, angle):
    """
    Sets the servo angle using provided pulse width parameters.
    """
    pulse_width = MIN_PULSE + (angle * ((MAX_PULSE - MIN_PULSE) / 180))
    pulse_width = int(max(min(pulse_width, MAX_PULSE), MIN_PULSE))  # Ensure within bounds
    pi.set_servo_pulsewidth(pin, pulse_width)
    return pulse_width

def rotate_servo_horizontal(session, request, servo_pin_horizontal):
    """
    Rotates the horizontal servo by +20 or -20 degrees and updates session variable.
    """
    current_angle = session.get('current_angle_horizontal', 0)
    new_angle = current_angle + int(request.form['angle'])
    
    # Check if new angle exceeds 180 degrees or goes below 0 degrees
    if new_angle > 180:
        new_angle = 180
    elif new_angle < 0:
        new_angle = 0
    
    set_servo_angle(servo_pin_horizontal, new_angle)
    session['current_angle_horizontal'] = new_angle
    return 'Horizontal servo rotated {} degrees (current angle: {})'.format(request.form['angle'], new_angle)

def rotate_servo_vertical(session, request, servo_pin_vertical):
    """
    Rotates the vertical servo by +20 or -20 degrees and updates session variable.
    """
    current_angle = session.get('current_angle_vertical', 0)
    new_angle = current_angle + int(request.form['angle'])
    
    # Check if new angle exceeds 180 degrees or goes below 0 degrees
    if new_angle > 80:
        new_angle = 80
    elif new_angle < 0:
        new_angle = 0
    
    set_servo_angle(servo_pin_vertical, new_angle)
    session['current_angle_vertical'] = new_angle
    return 'Vertical servo rotated {} degrees (current angle: {})'.format(request.form['angle'], new_angle)
