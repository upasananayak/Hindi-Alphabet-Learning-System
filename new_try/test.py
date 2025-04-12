import cv2

# Path to your image file; update this path if needed.
image_path = "letter_images/27_ra.png"

# Attempt to load the image.
img = cv2.imread(image_path)

if img is None:
    print("Failed to load image at:", image_path)
else:
    print("Image loaded successfully with shape:", img.shape)
    cv2.imshow("Loaded Image", img)
    cv2.waitKey(0)  # Wait indefinitely until a key is pressed.
    cv2.destroyAllWindows()
