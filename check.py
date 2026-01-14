""" Check.py """
""" This code is a verification and check form for the file uploaded by the user to see if it is valid for the analysis model. """

import os
import cv2
import numpy as np


# Configuration (Balanced Mobile-Friendly)
MIN_WIDTH = 150
MIN_HEIGHT = 150
BLUR_THRESHOLD = 30
SKIN_RATIO_THRESHOLD = 0.15
TARGET_SIZE = (224, 224)


# Resolution Check
def check_resolution(img, min_w=MIN_WIDTH, min_h=MIN_HEIGHT):
    h, w = img.shape[:2]
    return w >= min_w and h >= min_h


# Blur Detection
def is_blurry(img, threshold=BLUR_THRESHOLD):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return lap_var < threshold, lap_var


# Skin Texture Analysis
def analyze_skin_texture(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lap = cv2.Laplacian(gray, cv2.CV_64F)
    texture_var = lap.var()

    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size

    std_dev = np.std(gray)

    is_skin_like = (
        30 < texture_var < 1200 and
        edge_density < 0.30 and
        15 < std_dev < 120
    )

    texture_score = {
        "texture_variance": round(texture_var, 2),
        "edge_density": round(edge_density, 4),
        "std_deviation": round(std_dev, 2)
    }

    return is_skin_like, texture_score


# Skin Ratio Detection (HSV + YCrCb)
def skin_ratio_hsv(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([0, 20, 50], dtype=np.uint8)
    upper_hsv = np.array([25, 170, 255], dtype=np.uint8)
    mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    lower_ycrcb = np.array([0, 130, 75], dtype=np.uint8)
    upper_ycrcb = np.array([255, 180, 130], dtype=np.uint8)
    mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

    combined_mask = cv2.bitwise_and(mask_hsv, mask_ycrcb)

    skin_pixels = np.sum(combined_mask > 0)
    total_pixels = combined_mask.size

    return skin_pixels / total_pixels


# Resize & Normalize 
def resize_for_model(img, target_size=TARGET_SIZE):
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# Main Validation Pipeline
def analyze_image(path):
    response = {
        "status": None,
        "reason": None,
        "message": None,
        "details": {},
        "processed_image": None
    }

    # File check
    if not os.path.exists(path):
        response.update({
            "status": "error",
            "reason": "file_not_found",
            "message": "File not found"
        })
        return response

    # Load image
    img = cv2.imread(path)
    if img is None:
        response.update({
            "status": "error",
            "reason": "invalid_image",
            "message": "Invalid or corrupted image file"
        })
        return response

    # Resolution check
    h, w = img.shape[:2]
    response["details"]["original_resolution"] = f"{w}x{h}"

    if not check_resolution(img):
        response.update({
            "status": "error",
            "reason": "low_resolution",
            "message": f"Image resolution too low (minimum {MIN_WIDTH}x{MIN_HEIGHT})"
        })
        return response

    # Blur detection
    blurry, lap_var = is_blurry(img)
    response["details"]["laplacian_variance"] = round(lap_var, 2)

    # Skin ratio
    ratio = skin_ratio_hsv(img)
    response["details"]["skin_ratio"] = round(ratio, 4)

    # Texture analysis
    is_skin_texture, texture_data = analyze_skin_texture(img)
    response["details"]["texture_analysis"] = texture_data
    response["details"]["skin_texture_detected"] = is_skin_texture

    
    # Hard Rejection Rules
    if texture_data["edge_density"] > 0.35:
        response.update({
            "status": "error",
            "reason": "not_skin_pattern",
            "message": "Image contains patterns inconsistent with skin"
        })
        return response

    if texture_data["texture_variance"] > 1500:
        response.update({
            "status": "error",
            "reason": "not_skin_texture",
            "message": "Image texture inconsistent with skin"
        })
        return response

    if ratio < SKIN_RATIO_THRESHOLD:
        response.update({
            "status": "error",
            "reason": "not_skin",
            "message": "Insufficient skin area detected"
        })
        return response

    if blurry:
        response.update({
            "status": "error",
            "reason": "blurry",
            "message": "Image is too blurry for analysis"
        })
        return response

    # Reject smooth skin (no lesion)
    if ratio >= SKIN_RATIO_THRESHOLD and texture_data["texture_variance"] < 35:
        response.update({
            "status": "error",
            "reason": "no_lesion_detected",
            "message": "No visible skin lesion detected. Please capture the affected area clearly."
        })
        return response

    
    # Final preprocessing
    processed_img = resize_for_model(img)
    response["details"]["final_resolution"] = "224x224"
    response["processed_image"] = processed_img

    response.update({
        "status": "valid",
        "message": "Image is valid and ready for analysis"
    })

    return response