import keras
from keras.models import load_model
import imutils
from collections import deque
import cv2
import pandas as pd
from keras import layers
import numpy as np
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
import keras.backend as k

# Define letter_count globally so it's accessible throughout the script.
letter_count = {
    0: 'CHECK', 1: '01_ka', 2: '02_kha', 3: '03_ga', 4: '04_gha', 5: '05_kna',
    6: 'character_06_cha', 7: '07_chha', 8: '08_ja', 9: '09_jha', 10: '10_yna',
    11: '11_taamatar', 12: '12_thaa', 13: '13_daa', 14: '14_dhaa', 15: '15_adna',
    16: '16_tabala', 17: '17_tha', 18: '18_da', 19: '19_dha', 20: '20_na', 21: '21_pa',
    22: '22_pha', 23: '23_ba', 24: '24_bha', 25: '25_ma', 26: '26_yaw', 27: '27_ra',
    28: '28_la', 29: '29_waw', 30: '30_motosaw', 31: '31_petchiryakha', 32: '32_patalosaw',
    33: '33_ha', 34: '34_chhya', 35: '35_tra', 36: '36_gya', 37: 'CHECK'
}

# Make sure you load your trained model (model1) before using it in the prediction function.
# For example:
# model1 = load_model('your_model_path.keras')

def keras_process_image(img):
    image_x = 32
    image_y = 32
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img

def keras_predict(model, image):
    processed = keras_process_image(image)
    print("processed: " + str(processed.shape))
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def main():
    # Your main function can contain any additional setup if needed.
    pass

# Set up the webcam using the built-in camera (index 0)
cap = cv2.VideoCapture(0)

# Define the HSV range for green (adjust these values as needed)
Lower_green = np.array([110, 50, 50])
Upper_green = np.array([130, 255, 255])
pred_class = 0
pts = deque(maxlen=512)
blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
digit = np.zeros((200, 200, 3), dtype=np.uint8)

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    if ret:
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, Lower_green, Upper_green)
        blur = cv2.medianBlur(mask, 15)
        blur = cv2.GaussianBlur(blur, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        center = None
        if len(contours) >= 1:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 250:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                # Ensure center is computed before drawing it
                M = cv2.moments(contour)
                if M['m00'] != 0:
                    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                    pts.appendleft(center)
                    cv2.circle(img, center, 5, (0, 0, 255), -1)
                    for i in range(1, len(pts)):
                        if pts[i - 1] is None or pts[i] is None:
                            continue
                        cv2.line(blackboard, pts[i - 1], pts[i], (255, 255, 255), 10)
                        cv2.line(img, pts[i - 1], pts[i], (0, 0, 255), 5)
        else:
            if len(pts) != 0:
                blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
                blur1 = cv2.medianBlur(blackboard_gray, 15)
                blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
                thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                blackboard_cnts = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
                if len(blackboard_cnts) >= 1:
                    cnt = max(blackboard_cnts, key=cv2.contourArea)
                    print("Contour area:", cv2.contourArea(cnt))
                    if cv2.contourArea(cnt) > 2000:
                        x, y, w, h = cv2.boundingRect(cnt)
                        digit = blackboard_gray[y:y + h, x:x + w]
                        # Assuming model1 is already loaded and defined
                        pred_probab, pred_class = keras_predict(devanagari.h5, digit)
                        print("Prediction:", pred_class, "Probability:", pred_probab)
                pts = deque(maxlen=512)
                blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
        # Use the globally defined letter_count dictionary here.
        cv2.putText(img, "Conv Network :  " + str(letter_count[pred_class]), (10, 470),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Frame", img)
        cv2.imshow("Contours", thresh)
        if cv2.waitKey(27) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Optionally, call main() if needed
main()
