# Image Validation Module — Integration Guide

## Overview
This module validates uploaded images before analysis.  
It checks image resolution, blur level, and skin ratio, and rejects unsuitable inputs (e.g., non-skin, low-quality, or object images).

---

## Requirements
```bash
pip install -r requirements.txt
```

**requirements.txt**
```
opencv-python
numpy
Pillow
```

---

## Function
```python
from image_validation import analyze_image

result = analyze_image("path_to_image.jpg")
print(result)
```

---

## Example Output
```json
{
  "status": "VALID",
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
| Status | Reason | Message |
|---------|---------|----------|
| VALID | — | Image is valid and ready for analysis |
| REJECTED | low_resolution | Image resolution too low (minimum 224x224) |
| REJECTED | blurry | Image is too blurry for analysis |
| REJECTED | not_skin | Insufficient skin area detected |
| REJECTED | not_skin_pattern | Pattern inconsistent with skin (likely object/wall) |
| REJECTED | not_skin_texture | Texture too rough (likely furniture/object) |

---

## Integration Notes
- The function returns a Python dictionary (JSON ready).
- It can be wrapped inside an endpoint `/validate-image` in Flask or FastAPI.
- Expected use flow:
  1. Backend receives uploaded file.
  2. Calls `analyze_image()` with the file path.
  3. Returns the JSON result to the front-end.

---

## Maintainer
AI Engineer: [Your Name]  
Version: 1.0  
Last Updated: [Date]
