from flask import Flask, Response, render_template, request, session
import subprocess
import os
import pigpio
import RPi.GPIO as GPIO
from camera import generate_frames
from emailsend import send_email, email_sender_thread
from servo import rotate_servo_horizontal, rotate_servo_vertical, pi

app = Flask(__name__)
app.secret_key = '1'

# Define servo GPIO pins
servo_pin_horizontal = 27  # GPIO 17 for horizontal movement
servo_pin_vertical = 17    # GPIO 27 for vertical movement

# Set servo pins as PWM outputs
pi.set_mode(servo_pin_horizontal, pigpio.OUTPUT)
pi.set_mode(servo_pin_vertical, pigpio.OUTPUT)

@app.route('/')
def index():
    """
    Renders the main page with the buttons.
    """
    session.setdefault('current_angle_horizontal', 0)  # Initialize horizontal angle if not set
    session.setdefault('current_angle_vertical', 0)    # Initialize vertical angle if not set
    return render_template('index.html', 
                           current_angle_horizontal=session['current_angle_horizontal'],
                           current_angle_vertical=session['current_angle_vertical'])

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cgi-bin/forward.cgi')
def forward():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/jgy370/forward.sh'])
    return "Success"

@app.route('/cgi-bin/left.cgi')
def left():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/jgy370/left.sh'])
    return "Success"

@app.route('/cgi-bin/right.cgi')
def right():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/jgy370/right.sh'])
    return "Success"

@app.route('/cgi-bin/reverse.cgi')
def reverse():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/jgy370/reverse.sh'])
    return "Success"

@app.route('/cgi-bin/stop.cgi')
def stop():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/jgy370/stop.sh'])
    return "Success"

@app.route('/cgi-bin/buzzer_off.cgi')
def buzzer_off():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/buzzer/buzzer_off.sh'])
    return "Success"

@app.route('/cgi-bin/buzzer_on.cgi')
def buzzer_on():
    subprocess.call(['/home/pi/Desktop/picamera/scripts/buzzer/buzzer_on.sh'])
    return "Success"

@app.route('/rotate_horizontal', methods=['POST'])
def rotate_horizontal():
    return rotate_servo_horizontal(session, request, servo_pin_horizontal)

@app.route('/rotate_vertical', methods=['POST'])
def rotate_vertical():
    return rotate_servo_vertical(session, request, servo_pin_vertical)

if __name__ == '__main__':
    try:
        # Run Flask app
        app.run(host='192.168.244.170', port=5000)

    except KeyboardInterrupt:
        pi.stop()
