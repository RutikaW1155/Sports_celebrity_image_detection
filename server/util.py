import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import w2d

# Global variables for class mappings and model
__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def classify_image(image_base64_data, file_path=None):
    """
    Classifies the image provided in base64 format or from a file path.
    
    :param image_base64_data: Base64 encoded image data (optional if file_path is provided)
    :param file_path: File path to the image (optional if image_base64_data is provided)
    :return: List of dictionaries containing classification results
    """
    if __model is None or not __class_number_to_name:
        raise RuntimeError("Model or class dictionary not loaded.")

    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
    if not imgs:
        return []

    result = []
    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32 * 32 * 3, 1), scalled_img_har.reshape(32 * 32, 1)))

        len_image_array = 32 * 32 * 3 + 32 * 32
        final = combined_img.reshape(1, len_image_array).astype(float)
        prediction = __model.predict(final)[0]
        result.append({
            'class': class_number_to_name(prediction),
            'class_probability': np.around(__model.predict_proba(final) * 100, 2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })

    return result

def class_number_to_name(class_num):
    """Convert class number to class name."""
    return __class_number_to_name.get(class_num, "Unknown")

def load_saved_artifacts():
    """Load model and class dictionary from saved artifacts."""
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name
    global __model

    try:
        with open(r"D:\ML_SPORTS_PROJECT\server\artifacts\class_dictionary.json", "r") as f:
            __class_name_to_number = json.load(f)
            __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}
    except FileNotFoundError as e:
        print(f"Error loading class dictionary: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from class dictionary: {e}")
        return

    if __model is None:
        try:
            with open(r'D:\ML_SPORTS_PROJECT\server\artifacts\saved_model.pkl', 'rb') as f:
                __model = joblib.load(f)
        except FileNotFoundError as e:
            print(f"Error loading model: {e}")
            return
        except Exception as e:
            print(f"Error loading model: {e}")
            return
    print("loading saved artifacts...done")

def get_cv2_image_from_base64_string(b64str):
    """
    Convert a base64 encoded image string to a CV2 image.
    
    :param b64str: Base64 encoded image string
    :return: CV2 image
    """
    try:
        encoded_data = b64str.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Error decoding base64 image: {e}")
        return None

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    """
    Detect and crop faces with at least 2 eyes from an image.
    
    :param image_path: Path to the image file (optional if image_base64_data is provided)
    :param image_base64_data: Base64 encoded image data (optional if image_path is provided)
    :return: List of cropped face images
    """
    face_cascade = cv2.CascadeClassifier(r'D:\ML_SPORTS_PROJECT\server\opencv\haarcascades\haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(r'D:\ML_SPORTS_PROJECT\server\opencv\haarcascades\haarcascade_eye.xml')

    img = cv2.imread(image_path) if image_path else get_cv2_image_from_base64_string(image_base64_data)

    if img is None:
        print("Error: Could not read image.")
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    return cropped_faces

def get_b64_test_image_for_virat():
    """
    Get a base64 encoded test image for 'Virat'.
    
    :return: Base64 encoded image string
    """
    try:
        with open(r"D:\ML_SPORTS_PROJECT\server\b64.txt") as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"Error reading base64 test image file: {e}")
        return None

if __name__ == '__main__':
    load_saved_artifacts()
    b64_test_image = get_b64_test_image_for_virat()
    if b64_test_image:
        print(classify_image(b64_test_image))
    else:
        print("Error: Base64 test image data could not be loaded.")
