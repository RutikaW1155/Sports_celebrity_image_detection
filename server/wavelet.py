import numpy as np
import pywt
import cv2

def w2d(img, mode='haar', level=1):
    """
    Apply a wavelet transform to an image and return the transformed image.
    
    :param img: Input image (must be in RGB format).
    :param mode: Wavelet transform type. Default is 'haar'.
    :param level: Level of wavelet decomposition. Default is 1.
    :return: Image after applying wavelet transform.
    """
    try:
        # Convert to grayscale if the image is in RGB format
        if len(img.shape) == 3 and img.shape[2] == 3:  # Check if the image has 3 channels (RGB)
            imArray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            imArray = img

        # Convert to float32 and normalize
        imArray = np.float32(imArray)
        imArray /= 255.0

        # Compute wavelet coefficients
        coeffs = pywt.wavedec2(imArray, mode, level=level)

        # Process coefficients: Zero out approximation coefficients
        coeffs_H = list(coeffs)
        coeffs_H[0] *= 0

        # Reconstruct the image from the modified coefficients
        imArray_H = pywt.waverec2(coeffs_H, mode)
        imArray_H *= 255.0
        imArray_H = np.uint8(imArray_H)

        return imArray_H

    except Exception as e:
        print(f"Error in wavelet transform: {e}")
        return None
