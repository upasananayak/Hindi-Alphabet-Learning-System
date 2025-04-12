from flask import Flask, request, jsonify
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os

# Suppress TensorFlow logs if desired
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

# Load your trained model
model = load_model('devanagari.h5')
print("Model loaded successfully.")

def keras_process_image(img):
    """
    Process the input image:
      - Convert the input (2D list or numpy array) into a NumPy array.
      - Resize to 32x32 if needed.
      - Reshape to (-1, 32, 32, 1) for prediction.
    """
    image_x, image_y = 32, 32
    img = np.array(img, dtype=np.float32)
    if img.shape != (image_x, image_y):
        img = cv2.resize(img, (image_x, image_y))
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img

def keras_predict(model, image):
    """
    Predicts the class for the input image using the provided model.
    Returns the maximum probability and the predicted class index.
    """
    processed = keras_process_image(image)
    print("Processed image shape:", processed.shape)
    pred_probab = model.predict(processed)[0]
    pred_class = int(np.argmax(pred_probab))
    return float(np.max(pred_probab)), pred_class

@app.route('/predict', methods=['POST'])
def predict():
    """
    Expects a JSON payload with an 'input' key containing a 32x32 array of normalized pixel values.
    Returns the predicted class and probability.
    """
    try:
        data = request.get_json(force=True)
        if 'input' not in data:
            return jsonify({'error': 'No input provided in the JSON payload.'}), 400
        input_data = data['input']
        prob, pred_class = keras_predict(model, input_data)
        return jsonify({'predicted_class': pred_class, 'probability': prob})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
