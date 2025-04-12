from flask import Flask, Response, jsonify, send_from_directory
import threading
import cv2
import numpy as np
from collections import deque
import os
import keras
from keras.models import load_model

app = Flask(__name__)

# Define letter_count mapping (keys correspond to model prediction indices)
letter_count = {
    0: 'CHECK', 1: '01_ka', 2: '02_kha', 3: '03_ga', 4: '04_gha', 5: '05_kna',
    6: 'character_06_cha', 7: '07_chha', 8: '08_ja', 9: '09_jha', 10: '10_yna',
    11: '11_taamatar', 12: '12_thaa', 13: '13_daa', 14: '14_dhaa', 15: '15_adna',
    16: '16_tabala', 17: '17_tha', 18: '18_da', 19: '19_dha', 20: '20_na', 21: '21_pa',
    22: '22_pha', 23: '23_ba', 24: '24_bha', 25: '25_ma', 26: '26_yaw', 27: '27_ra',
    28: '28_la', 29: '29_waw', 30: '30_motosaw', 31: '31_petchiryakha', 32: '32_patalosaw',
    33: '33_ha', 34: '34_chhya', 35: '35_tra', 36: '36_gya', 37: 'CHECK'
}

# Folder where predefined letter images are stored.
LETTER_IMAGE_FOLDER = "letter_images"
STATIC_FOLDER = "static"

# Ensure static folder exists
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Global variable to hold the latest predicted letter image (BGR, 350x480)
latest_letter_image = np.zeros((480, 350, 3), dtype=np.uint8)

# Load your trained model (ensure 'devanagari.h5' is in the same directory)
model1 = load_model('devanagari.h5')
print("Model loaded successfully.")

def keras_process_image(img):
    image_x, image_y = 32, 32
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img

def keras_predict(model, image):
    processed = keras_process_image(image)
    print("Processed image shape:", processed.shape)
    pred_probab = model.predict(processed)[0]
    pred_class = int(np.argmax(pred_probab))
    return float(np.max(pred_probab)), pred_class

def run_camera_capture():
    global latest_letter_image

    cap = cv2.VideoCapture(0)  # Use built-in camera (index 0)
    Lower_green = np.array([40, 50, 50])
    Upper_green = np.array([80, 255, 255])
    
    pred_class = 0
    pts = deque(maxlen=512)
    blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
    # Initialize 'digit' as a blank grayscale image
    digit = np.zeros((200, 200), dtype=np.uint8)
    
    while True:
        ret, img = cap.read()
        if not ret:
            break
        img = cv2.flip(img, 1)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, Lower_green, Upper_green)
        blur = cv2.medianBlur(mask, 15)
        blur = cv2.GaussianBlur(blur, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        center = None

        if len(contours) >= 1:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 250:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                M = cv2.moments(contour)
                if M['m00'] != 0:
                    center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
                    pts.appendleft(center)
                    cv2.circle(img, center, 5, (0, 0, 255), -1)
                    for i in range(1, len(pts)):
                        if pts[i-1] is None or pts[i] is None:
                            continue
                        cv2.line(blackboard, pts[i-1], pts[i], (255, 255, 255), 10)
                        cv2.line(img, pts[i-1], pts[i], (0, 0, 255), 5)
        else:
            if len(pts) != 0:
                blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
                blur1 = cv2.medianBlur(blackboard_gray, 15)
                blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
                thresh1 = cv2.threshold(blur1, 0, 255,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                blackboard_cnts = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
                if len(blackboard_cnts) >= 1:
                    cnt = max(blackboard_cnts, key=cv2.contourArea)
                    print("Contour area:", cv2.contourArea(cnt))
                    if cv2.contourArea(cnt) > 2000:
                        x, y, w, h = cv2.boundingRect(cnt)
                        digit = blackboard_gray[y:y+h, x:x+w]
                        pred_probab, pred_class = keras_predict(model1, digit)
                        print("Prediction:", letter_count[pred_class], "Probability:", pred_probab)
                        # Load predefined image for predicted letter.
                        letter_name = letter_count.get(pred_class, "Unknown")
                        letter_image_path = os.path.join(LETTER_IMAGE_FOLDER, f"{letter_name}.png")
                        print("Looking for image at:", letter_image_path)
                        if os.path.exists(letter_image_path):
                            predefined_letter = cv2.imread(letter_image_path)
                            if predefined_letter is None:
                                print("Failed to load image:", letter_image_path)
                                predefined_letter = np.zeros((480, 350, 3), dtype=np.uint8)
                            else:
                                predefined_letter = cv2.resize(predefined_letter, (350, 480))
                                print("Predefined image loaded, shape:", predefined_letter.shape)
                        else:
                            print("Image not found:", letter_image_path)
                            predefined_letter = np.zeros((480, 350, 3), dtype=np.uint8)
                        # Update global latest_letter_image
                        latest_letter_image = predefined_letter.copy()
                pts = deque(maxlen=512)
                blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Overlay the predicted label on the frame.
        cv2.putText(img, "Predicted: " + str(letter_count[pred_class]),
                    (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Ensure 'digit' is in color for stacking. Resize it to 350x480.
        if len(digit.shape) == 2:
            digit_bgr = cv2.cvtColor(digit, cv2.COLOR_GRAY2BGR)
        else:
            digit_bgr = digit
        digit_bgr = cv2.resize(digit_bgr, (350, 480))
        
        # Combine the drawn letter and the predefined letter side by side.
        combined = np.hstack((digit_bgr, latest_letter_image))
        cv2.imshow("Letter Comparison", combined)
        cv2.imshow("Frame", img)
        
        # Encode the frame as JPEG.
        ret2, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def generate_frames():
    for frame in run_camera_capture():
        yield frame

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/predicted_letter')
def predicted_letter():
    global latest_letter_image
    ret, buffer = cv2.imencode('.jpg', latest_letter_image)
    if ret:
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    else:
        return "Error encoding image", 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

@app.route('/')
def index():
    html = '''
    <html>
      <head>
        <title>Devanagari Letter Adventure!</title>
        <style>
          body { 
            text-align: center; 
            font-family: 'Comic Sans MS', cursive, sans-serif; 
            background-color: #ffebee;
            margin: 0; 
            padding: 0;
            background-image: url('https://cdnjs.cloudflare.com/ajax/libs/simple-icons/3.0.1/simple-icons.svg'), linear-gradient(to bottom, #ffebee, #fff9c4);
            background-blend-mode: overlay;
            background-size: 200px;
            background-attachment: fixed;
            overflow-x: hidden;
            position: relative;
          }
          .header { 
            background-color: #ffce4b; 
            padding: 10px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-bottom: 5px dashed #ff6f61;
            margin-bottom: 20px;
            position: relative;
            z-index: 2;
          }
          h1 { 
            color: #ff5722; 
            text-shadow: 2px 2px 0px #ffffff, 3px 3px 0px #ff9e80; 
            margin: 15px 0;
            font-size: 2.5em;
            letter-spacing: 1px;
          }
          .top-image {
            display: block;
            margin: 0 auto;
            width: 700px;
            height: 250px;
            border-radius: 20px;
            border: 5px solid #8bc34a;
          }
          .container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 2;
          }
          .panel {
            background-color: white;
            border-radius: 25px;
            padding: 20px;
            box-shadow: 0 8px 0 #cddc39, 0 12px 20px rgba(0,0,0,0.2);
            transition: all 0.3s;
            border: 4px solid #4caf50;
          }
          .panel:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 0 #cddc39, 0 18px 20px rgba(0,0,0,0.2);
          }
          h3 {
            color: #9c27b0;
            margin-top: 0;
            font-size: 1.8em;
            text-shadow: 1px 1px 0px #ffffff;
          }
          .video-feed, .letter-image {
            border-radius: 15px;
            border: 6px solid #03a9f4;
            box-shadow: 0 0 0 4px #ffeb3b;
          }
          .footer {
            background-color: #ffce4b;
            padding: 15px;
            margin-top: 30px;
            color: #ff5722;
            border-top: 5px dashed #ff6f61;
            font-size: 1.2em;
            font-weight: bold;
            position: relative;
            z-index: 2;
          }
          .star {
            display: inline-block;
            animation: spin 5s linear infinite;
            margin: 0 10px;
            font-size: 1.5em;
          }
          .bubble {
            position: absolute;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: radial-gradient(circle at 10px 10px, rgba(255,255,255,0.8), rgba(100,181,246,0.4));
            animation: float 12s ease-in-out infinite;
            z-index: 1;
            pointer-events: none;
          }
          .balloon {
            position: absolute;
            animation: float-balloon 15s ease-in-out infinite;
            z-index: 1;
            pointer-events: none;
          }
          /* Balloon shape with CSS */
          .balloon-body {
            width: 50px;
            height: 60px;
            background: radial-gradient(circle at 30% 30%, 
              var(--balloon-light), var(--balloon-color));
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            position: relative;
          }
          .balloon-string {
            position: absolute;
            width: 2px;
            height: 70px;
            background-color: rgba(0,0,0,0.5);
            left: 50%;
            top: 95%;
            transform: translateX(-50%);
          }
          .balloon-tie {
            position: absolute;
            width: 10px;
            height: 10px;
            background-color: var(--balloon-color);
            border-radius: 50%;
            bottom: -5px;
            left: 50%;
            transform: translateX(-50%);
          }
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); }
            25% { transform: translateY(-40px) translateX(20px); }
            50% { transform: translateY(-60px) translateX(-20px); }
            75% { transform: translateY(-20px) translateX(40px); }
          }
          @keyframes float-balloon {
            0% { transform: translateY(100vh) translateX(0) rotate(0deg); }
            100% { transform: translateY(-200px) translateX(50px) rotate(5deg); }
          }
          .motivational {
            font-size: 1.3em;
            color: #e91e63;
            margin: 15px 0;
            font-weight: bold;
            text-shadow: 1px 1px 0px #ffffff;
          }
          .instructions {
            background-color: #e3f2fd;
            border-radius: 15px;
            padding: 10px;
            margin: 10px auto;
            max-width: 800px;
            border: 3px dotted #2196f3;
            font-size: 1.1em;
            position: relative;
            z-index: 2;
          }
          /* Cloud element for additional fun */
          .cloud {
            position: absolute;
            background: #fff;
            border-radius: 50%;
            box-shadow: 
              10px 10px 0 0 #fff,
              20px 10px 0 0 #fff,
              30px 10px 0 0 #fff,
              15px 0px 0 0 #fff,
              25px 0px 0 0 #fff;
            height: 25px;
            width: 40px;
            animation: cloud-float 30s linear infinite;
            opacity: 0.8;
            z-index: 1;
          }
          @keyframes cloud-float {
            0% { transform: translateX(-100px); }
            100% { transform: translateX(calc(100vw + 100px)); }
          }
          @media (max-width: 1000px) {
            .container {
              flex-direction: column;
            }
          }
        </style>
      </head>
      <body onload="createBackgroundElements()">
        <div class="header">
          <img class="top-image" src="/static/image.png" alt="Devanagari Alphabet" />
          <h1>
            <span class="star">✨</span>
            Devanagari Learning Adventure!
            <span class="star">✨</span>
          </h1>
          <p class="motivational">Let's learn Devanagari letters together!</p>
        </div>
        
        <div class="instructions">
          <p>👉 Use a <strong>green</strong> object to draw in the air! ✏️write any letter to get see a drawing!</p>
        </div>
        
        <div class="container">
          <div class="panel">
            <h3>📹 Your Magic Drawing Space</h3>
            <img class="video-feed" src="/video_feed" width="640" height="480" />
          </div>
          <div class="panel">
            <h3>✨ Letter of Wonder ✨</h3>
            <img id="predictedLetter" class="letter-image" src="/predicted_letter" width="350" height="480" />
          </div>
        </div>
        
        <div class="footer">
          <p>🎉 You're doing AMAZING! Keep practicing! 🎉</p>
          <p>Every letter you learn is a new superpower! 💪</p>
        </div>
        
        <script>
          // Update the predicted letter image every 2 seconds to force a refresh
          setInterval(function(){
              var predLetterImg = document.getElementById("predictedLetter");
              predLetterImg.src = "/predicted_letter?time=" + new Date().getTime();
          }, 2000);
          
          // Create floating bubbles, balloons, and clouds for fun background
          function createBackgroundElements() {
            const body = document.querySelector('body');
            
            // Create bubbles (more of them now)
            for (let i = 0; i < 40; i++) {
              const bubble = document.createElement('div');
              bubble.className = 'bubble';
              bubble.style.left = Math.random() * 100 + 'vw';
              bubble.style.top = Math.random() * 100 + 'vh';
              bubble.style.width = (Math.random() * 30 + 20) + 'px';
              bubble.style.height = bubble.style.width;
              bubble.style.animationDuration = (Math.random() * 10 + 5) + 's';
              bubble.style.animationDelay = (Math.random() * 5) + 's';
              body.appendChild(bubble);
            }
            
            // Create balloons (colorful and fun)
            const balloonColors = [
              '#ff5252', '#ff4081', '#e040fb', '#7c4dff', 
              '#536dfe', '#448aff', '#40c4ff', '#18ffff',
              '#64ffda', '#69f0ae', '#b2ff59', '#eeff41',
              '#ffff00', '#ffd740', '#ffab40', '#ff6e40'
            ];
            
            for (let i = 0; i < 20; i++) {
              const balloon = document.createElement('div');
              balloon.className = 'balloon';
              
              const balloonColor = balloonColors[Math.floor(Math.random() * balloonColors.length)];
              const balloonBody = document.createElement('div');
              balloonBody.className = 'balloon-body';
              balloonBody.style.setProperty('--balloon-color', balloonColor);
              balloonBody.style.setProperty('--balloon-light', lightenColor(balloonColor, 30));
              
              const balloonString = document.createElement('div');
              balloonString.className = 'balloon-string';
              
              const balloonTie = document.createElement('div');
              balloonTie.className = 'balloon-tie';
              balloonTie.style.backgroundColor = balloonColor;
              
              balloonBody.appendChild(balloonTie);
              balloon.appendChild(balloonBody);
              balloon.appendChild(balloonString);
              
              balloon.style.left = (Math.random() * 90 + 5) + 'vw';
              balloon.style.animationDuration = (Math.random() * 20 + 15) + 's';
              balloon.style.animationDelay = (Math.random() * 10) + 's';
              
              body.appendChild(balloon);
            }
            
            // Create clouds floating across the screen
            for (let i = 0; i < 5; i++) {
              const cloud = document.createElement('div');
              cloud.className = 'cloud';
              cloud.style.top = (Math.random() * 30 + 5) + 'vh';
              cloud.style.animationDuration = (Math.random() * 60 + 30) + 's';
              cloud.style.animationDelay = (Math.random() * 30) + 's';
              cloud.style.transform = 'scale(' + (Math.random() * 1.5 + 0.8) + ')';
              body.appendChild(cloud);
            }
          }
          
          // Helper function to lighten colors for balloon gradient
          function lightenColor(color, percent) {
            const num = parseInt(color.replace('#', ''), 16),
                  amt = Math.round(2.55 * percent),
                  R = (num >> 16) + amt,
                  G = (num >> 8 & 0x00FF) + amt,
                  B = (num & 0x0000FF) + amt;
            return '#' + (0x1000000 + (R<255?R<1?0:R:255)*0x10000 + (G<255?G<1?0:G:255)*0x100 + (B<255?B<1?0:B:255)).toString(16).slice(1);
          }
        </script>
      </body>
    </html>
    '''
    return html


if __name__ == '__main__':
    app.run(debug=True,port=5050)
