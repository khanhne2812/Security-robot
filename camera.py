# camera.py
from emailsend import send_email, email_sender_thread
import cv2
import numpy as np
import time
from picamera2 import Picamera2
import RPi.GPIO as GPIO
# Initialize Picamera2
piCam = Picamera2()
piCam.preview_configuration.main.size = (720, 480)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.controls.FrameRate = 30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

buzzer_pin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
# Load the MobileNet SSD model
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt', 'MobileNetSSD_deploy.caffemodel')

# Class labels for MobileNet SSD
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
def generate_frames():
    detection_counter = 0
    detection_threshold = 4  # seconds
    last_detection_time = time.time()
    start_time = time.time()
    frame_count = 0
    buzzer_on = False  # Flag to keep track of buzzer state

    while True:
        frame = piCam.capture_array()
        
        # Prepare the frame for object detection
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        
        # Draw rectangles around detected humans (person class)
        person_detected = False
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence >= 0.5:  # adjust confidence threshold as needed
                idx = int(detections[0, 0, i, 1])
                if CLASSES[idx] == "person":
                    person_detected = True
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
        
        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        
        # Display FPS on the frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Check for detections and update the counter
        current_time = time.time()
        if person_detected:
            if current_time - last_detection_time <= 1:
                detection_counter += current_time - last_detection_time
            else:
                detection_counter = 0  # reset if the interval is too long
            last_detection_time = current_time

            # Check if detection counter exceeds the threshold to turn on the buzzer
            if detection_counter >= detection_threshold:
                file_path = 'detected_people.jpg'
                cv2.imwrite(file_path, frame)
                email_sender_thread(file_path)
                detection_counter = 0  # reset after sending email
                if not buzzer_on:
                    GPIO.output(buzzer_pin, GPIO.HIGH)  # Turn on the buzzer
                    buzzer_on = True
        else:
            detection_counter = 0  # reset if no detection

            if buzzer_on:
                GPIO.output(buzzer_pin, GPIO.LOW)  # Turn off the buzzer
                buzzer_on = False
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')