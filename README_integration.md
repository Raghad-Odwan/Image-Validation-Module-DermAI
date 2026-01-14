# Image Validation Module — Integration Guide

## Overview

This module performs **technical validation checks** on uploaded images before they are passed to the AI classification model in the DermAI system.
Its purpose is to ensure that only images with sufficient quality and appropriate visual characteristics are forwarded for analysis.

This module does **not** perform medical diagnosis or disease detection.

---

## Purpose

The validation module is designed to:

* Filter invalid or corrupted image files
* Reject low-quality or unsuitable images
* Prevent non-skin or irrelevant images from reaching the AI model
* Improve system robustness and user feedback

---

## Validation Checks

The following checks are applied sequentially:

### 1. File Integrity

* Verifies that the file exists
* Ensures the image can be loaded correctly

### 2. Resolution Check

* Ensures minimum resolution requirements are met
* Prevents loss of information during resizing

### 3. Blur Detection

* Uses Laplacian variance to detect excessive blur
* Rejects images unsuitable for feature extraction

### 4. Skin Area Estimation

* Estimates the proportion of visible skin using HSV and YCrCb color spaces
* Rejects images with insufficient skin coverage

### 5. Texture Analysis

* Evaluates edge density, texture variance, and grayscale statistics
* Filters images with patterns inconsistent with typical skin texture
* Rejects overly smooth images where no lesion-like structure is visible

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

### requirements.txt

```
opencv-python
numpy
Pillow
```

---

## Usage

```python
from check import analyze_image

result = analyze_image("path_to_image.jpg")
print(result)
```

---

## Example Output

```json
{
  "status": "valid",
  "reason": null,
  "message": "Image is valid and ready for analysis",
  "details": {
    "original_resolution": "1024x1024",
    "laplacian_variance": 45.9,
    "skin_ratio": 0.32,
    "texture_analysis": {
      "texture_variance": 45.9,
      "edge_density": 0.021,
      "std_deviation": 54.3
    },
    "skin_texture_detected": true,
    "final_resolution": "224x224"
  }
}
```

---

## Possible Responses

| Status | Reason             | Description                                    |
| ------ | ------------------ | ---------------------------------------------- |
| valid  | —                  | Image passed all validation checks             |
| error  | file_not_found     | File path does not exist                       |
| error  | invalid_image      | File is corrupted or unreadable                |
| error  | low_resolution     | Image resolution below minimum requirement     |
| error  | blurry             | Image is too blurry for reliable analysis      |
| error  | not_skin           | Insufficient visible skin area detected        |
| error  | not_skin_pattern   | Image contains patterns inconsistent with skin |
| error  | not_skin_texture   | Image texture inconsistent with skin           |
| error  | no_lesion_detected | No visible lesion-like structure detected      |

---

## Output Description

The returned dictionary contains:

* `status`: Validation result (`valid` or `error`)
* `reason`: Rejection reason (if applicable)
* `message`: User-facing explanation
* `details`: Diagnostic metrics and intermediate values
* `processed_image`: Preprocessed image ready for model inference (only if valid)

---

## Integration Notes

* The function returns a Python dictionary that is JSON-ready.
* Intended to be used as a **pre-inference gatekeeper**.
* Typical backend workflow:

  1. Backend receives uploaded image.
  2. Calls `analyze_image()` with the file path.
  3. If status is `valid`, forwards the processed image to the AI classifier.
  4. If status is `error`, returns the validation message to the client.

---

## System Role

This module acts as an intermediate layer between user input and the AI classifier.
It improves system reliability by preventing unsuitable inputs from affecting classification and explainability stages.

---

## Limitations

* Validation is heuristic-based and may fail under extreme lighting conditions
* Skin detection relies on color-based thresholds
* This module evaluates **technical suitability only**, not medical correctness

---

## File Structure

```
Image-Validation-Module-DermAI/
├── check.py
└── README.md
```

---
**Raghad Mousleh**
AI Engineer


بس احكي 👍
