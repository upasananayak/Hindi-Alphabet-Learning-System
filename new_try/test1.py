from flask import Flask, Response, jsonify, send_from_directory
import threading
import cv2
import numpy as np
from collections import deque
import os
import keras
from keras.models import load_model
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not opened")
