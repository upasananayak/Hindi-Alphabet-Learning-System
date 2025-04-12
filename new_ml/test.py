import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D as OriginalDepthwiseConv2D

# Define a custom DepthwiseConv2D that ignores the 'groups' parameter.
class CustomDepthwiseConv2D(OriginalDepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        # Remove the 'groups' parameter if it exists.
        kwargs.pop('groups', None)
        super(CustomDepthwiseConv2D, self).__init__(*args, **kwargs)

# Define a custom CategoricalCrossentropy loss that replaces reduction='auto'
class CustomCategoricalCrossentropy(tf.keras.losses.CategoricalCrossentropy):
    def __init__(self, **kwargs):
        # If reduction is 'auto', change it to a supported value.
        if 'reduction' in kwargs and kwargs['reduction'] == 'auto':
            kwargs['reduction'] = tf.keras.losses.Reduction.SUM_OVER_BATCH_SIZE
        super().__init__(**kwargs)

# Create a dictionary for custom objects needed for loading the model.
custom_objects = {
    'DepthwiseConv2D': CustomDepthwiseConv2D,
    'categorical_crossentropy': CustomCategoricalCrossentropy,
    'CategoricalCrossentropy': CustomCategoricalCrossentropy
}

try:
    model = load_model("model.h5", custom_objects=custom_objects)
    print("Model loaded successfully.")
except Exception as e:
    print("Error loading model:", e)
