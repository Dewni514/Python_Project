import cv2
import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading

# Function to play an alarm sound
def play_alarm_sound():
    # Replace 'alarm.wav' with the path to your alarm sound file
    playsound('alarm.wav')

# Function to start the motion detection
def start_motion_detection():
    global is_detection_running
    is_detection_running = True
    thread = threading.Thread(target=detect_motion)
    thread.daemon = True
    thread.start()

# Function to stop the motion detection
def stop_motion_detection():
    global is_detection_running
    is_detection_running = False

# Function for motion detection
def detect_motion():
    global is_detection_running
    motion_threshold = 5000
    previous_frame = None

    while is_detection_running:
        ret, current_frame = cap.read()

        if not ret:
            break

        gray_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if previous_frame is None:
            previous_frame = gray_frame
            continue

        frame_delta = cv2.absdiff(previous_frame, gray_frame)
        _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) > motion_threshold:
                motion_detected = True
                break

        if motion_detected:
            play_alarm_sound()

        previous_frame = gray_frame

# Function to exit the program
def exit_program():
    stop_motion_detection()
    cap.release()
    root.destroy()

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create the main GUI window
root = tk.Tk()
root.title("Motion Detection and Alarm")

# Create GUI elements
start_button = tk.Button(root, text="Start Detection", command=start_motion_detection)
stop_button = tk.Button(root, text="Stop Detection", command=stop_motion_detection)
exit_button = tk.Button(root, text="Exit", command=exit_program)

# Place GUI elements on the window
start_button.pack()
stop_button.pack()
exit_button.pack()

# Initialize the detection status
is_detection_running = False

# Start the GUI main loop
root.mainloop()
