#2/20 final
import cv2
import mediapipe as mp
import time
import numpy as np
from IPython.display import display
import ipywidgets as widgets
from threading import Thread
from MangDang.mini_pupper.ESP32Interface import ESP32Interface
from MangDang.mini_pupper.Config import PWMParams

#PWMParams.servo_ids = np.array([[1]])
esp32 = ESP32Interface()
esp32.connect()


positions = [512] * 12
servo_yaw = 1
servo_pitch = 1

# range
yaw_min, yaw_max = 400, 574   #left and right
pitch_min, pitch_max = 400, 574


mp_face_detection = mp.solutions.face_detection
cap = cv2.VideoCapture(0)

# axis of center
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
screen_center_x = frame_width // 2
screen_center_y = frame_height // 2


tracker = cv2.TrackerKCF_create()
tracking = False


yaw_sensitivity = 0.05
pitch_sensitivity = 0.05
max_adjust = 30

image_widget = widgets.Image(format='jpeg', width=640, height=480)
stop_button = widgets.Button(description="Stop Camera")

running = True

def update_camera():
    global running, tracking, tracker, positions

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while running:
            success, image = cap.read()
            if not success:
                continue

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            if not tracking:
                results = face_detection.process(image_rgb)

                if results.detections:
                    for detection in results.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        h_img, w_img, _ = image.shape
                        x = int(bboxC.xmin * w_img)
                        y = int(bboxC.ymin * h_img)
                        w = int(bboxC.width * w_img)
                        h = int(bboxC.height * h_img)

                        if x < 0 or y < 0 or w <= 0 or h <= 0:
                            continue

                        tracker = cv2.TrackerKCF_create()
                        tracker.init(image, (x, y, w, h))
                        tracking = True
                        break

            else:
                success, bbox = tracker.update(image)
                if success:
                    x, y, w, h = [int(v) for v in bbox]
                    cx, cy = x + w // 2, y + h // 2


                    error_x = (cx - screen_center_x) / frame_width
                    error_y = (cy - screen_center_y) / frame_height


                    adjust_factor_x = min(1.0, abs(error_x) * 5)
                    adjust_factor_y = min(1.0, abs(error_y) * 5)


                    if abs(error_x) > yaw_sensitivity:
                        yaw_adjust = int(positions[servo_yaw - 1] + max_adjust * error_x * adjust_factor_x)
                        positions[servo_yaw - 1] = max(yaw_min, min(yaw_max, yaw_adjust))
                    '''
                    if abs(error_y) > pitch_sensitivity:
                        pitch_adjust = int(positions[servo_pitch - 1] + max_adjust * error_y * adjust_factor_y)
                        positions[servo_pitch - 1] = max(pitch_min, min(pitch_max, pitch_adjust))
                    '''

                    #torque = [1] * 12
                    esp32.servos_set_position(positions)


                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(image, f"C: {cx},{cy}", (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                else:
                    tracking = False


            _, frame_jpeg = cv2.imencode('.jpeg', image)
            image_widget.value = frame_jpeg.tobytes()

            time.sleep(0.05)

    cap.release()


def stop_camera(button):
    global running
    running = False
    stop_button.disabled = True

stop_button.on_click(stop_camera)

display(image_widget, stop_button)

thread = Thread(target=update_camera)
thread.start()
