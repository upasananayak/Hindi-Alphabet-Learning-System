import requests
from flask import Flask, request, jsonify, send_from_directory,render_template
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D as OriginalDepthwiseConv2D
import numpy as np
from PIL import Image
import io
import base64
import logging
import os
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DJANGO_API_URL = "http://127.0.0.1:8000/get_image_paths/"
# ---------------------------------------------------------------------------
# Define class mapping for Devanagari characters
classes = [
    'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ड़', 'त', 'थ', 'द', 'ध',
    'क', 'न', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल',
    'व', 'ख', 'श', 'ष', 'स', 'ह', 'छ', 'त्र', 'ज्ञ', 'ग',
    'घ', 'ङ', 'च', 'छ', 'ज', 'झ', '०', '१', '२', '३',
    '४', '५', '६', '७', '८', '९'
]

# ---------------------------------------------------------------------------
# Define a custom DepthwiseConv2D that ignores the 'groups' parameter.
class CustomDepthwiseConv2D(OriginalDepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop('groups', None)  # Remove 'groups' if it exists.
        super(CustomDepthwiseConv2D, self).__init__(*args, **kwargs)

# Define a custom CategoricalCrossentropy loss to handle reduction='auto'
class CustomCategoricalCrossentropy(tf.keras.losses.CategoricalCrossentropy):
    def __init__(self, **kwargs):
        if 'reduction' in kwargs and kwargs['reduction'] == 'auto':
            kwargs['reduction'] = tf.keras.losses.Reduction.SUM_OVER_BATCH_SIZE
        super().__init__(**kwargs)

# Create a dictionary for custom objects required for model loading.
custom_objects = {
    'DepthwiseConv2D': CustomDepthwiseConv2D,
    'categorical_crossentropy': CustomCategoricalCrossentropy,
    'CategoricalCrossentropy': CustomCategoricalCrossentropy
}

# ---------------------------------------------------------------------------
# Initialize the Flask app and enable CORS.
app = Flask(__name__)
CORS(app)  # Allow all origins
#DJANGO_STATIC_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'alphabet', 'static')
DJANGO_STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../alphabet/static'))

# ---------------------------------------------------------------------------
# Load the trained model (make sure "model.h5" is a complete model file)
MODEL_PATH = "model.h5"
try:
    model = load_model(MODEL_PATH, custom_objects=custom_objects)
    logger.info("Model loaded successfully.")
    logger.info(f"Model output shape: {model.output_shape}")
    num_classes = model.output_shape[-1]
    logger.info(f"Number of output classes: {num_classes}")
    
    # Verify class mapping matches model output
    if num_classes != len(classes):
        logger.warning(f"Model has {num_classes} output classes but mapping has {len(classes)} classes.")
        
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# ---------------------------------------------------------------------------
# Preprocessing function to match training:
def preprocess_image_from_base64(image_base64):
    try:
        # Remove header if present (e.g., 'data:image/png;base64,')
        if "base64," in image_base64:
            image_base64 = image_base64.split("base64,")[1]
        
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes)).convert("L")
        
        # Add preprocessing debug info
        logger.info(f"Original image size: {image.size}")
        
        # Center the image on a white background
        # Create a white background of size 32x32
        background = Image.new("L", (32, 32), 255)
        
        # Resize the character image while maintaining aspect ratio
        # Calculate the appropriate scale factor
        scale_factor = min(28 / image.width, 28 / image.height)
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Calculate position to paste (centering the character)
        paste_x = (32 - new_width) // 2
        paste_y = (32 - new_height) // 2
        
        # Paste the character onto the background
        background.paste(image, (paste_x, paste_y))
        image = background
        
        # Invert the colors so characters are white on black (like MNIST)
        image = Image.eval(image, lambda x: 255 - x)
        
        # Convert to numpy and normalize
        img_array = np.array(image).astype("float32") / 255.0
        
        # Log some statistics about the processed image
        logger.info(f"Processed image shape: {img_array.shape}")
        logger.info(f"Pixel value range: min={img_array.min()}, max={img_array.max()}")
        
        # Reshape for the model
        img_array = np.expand_dims(img_array, axis=-1)  # (32,32,1)
        img_array = np.expand_dims(img_array, axis=0)    # (1,32,32,1)
        
        return img_array
    
    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        raise

# ---------------------------------------------------------------------------
# Define the /predict endpoint.
@app.route("/predict", methods=["POST"])

def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        processed_image = preprocess_image_from_base64(data["image"])
        predictions = model.predict(processed_image)
        
        # Log raw predictions for debugging
        logger.info(f"Raw predictions shape: {predictions.shape}")
        
        predicted_class = int(np.argmax(predictions, axis=1)[0])
        confidence = float(np.max(predictions))
        
        # Get the corresponding Devanagari character
        predicted_char = classes[predicted_class] if predicted_class < len(classes) else f"Unknown ({predicted_class})"
        
        logger.info(f"Predicted class: {predicted_class}, Character: {predicted_char}, Confidence: {confidence}")
        
        # Return all class probabilities for debugging
        all_probs = {i: float(prob) for i, prob in enumerate(predictions[0])}
        
        return jsonify({
            "predicted_class": predicted_class,
            "predicted_char": predicted_char,
            "confidence": confidence,
            "all_probabilities": all_probs
        })
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# Add a test endpoint to verify the model is working
@app.route("/test", methods=["GET"])
def test():
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500
    
    return jsonify({
        "status": "ok", 
        "model_loaded": True,
        "output_shape": str(model.output_shape),
        "num_classes": len(classes),
        "classes": classes
    })

@app.route('/django-static/<path:filename>')
def django_static(filename):
    return send_from_directory(DJANGO_STATIC_PATH, filename)

@app.route('/index')
def index():
    order = request.args.get('order')  # Get order from URL
    if not order:
        return "Order not specified", 400
    
    # Fetch image paths from Django
    response = requests.get(f"{DJANGO_API_URL}{order}/")
    if response.status_code == 200:
        data = response.json()
        letter_path = data['letter_path']
        object_path = data['object_path']
    else:
        letter_path = object_path = None

    return render_template('index.html', letter_path=letter_path, object_path=object_path)



# ---------------------------------------------------------------------------
# Run the Flask app.
if __name__ == "__main__":
    app.run(port=5000, debug=True)