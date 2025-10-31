# DermAI - Image Validation Module
This module performs automated validation for uploaded images before analysis.
It checks image quality, resolution, blur level, and detects whether the content is actual skin or irrelevant objects.

The module ensures only valid dermatological images are sent to the main diagnostic model.
It returns structured JSON responses indicating the validation status, reason, and detailed metrics.

Designed for integration with backend endpoints (Flask/FastAPI).

Main features:

Automatic detection of invalid or low-quality images

Blur detection using Laplacian variance

Skin ratio and texture pattern analysis

Standardized JSON output for backend consumption

Files included:

image_validation.py – Core function (analyze_image())

Check.ipynb – Jupyter notebook for development and testing

requirements.txt – Dependencies list

README_integration.md – Integration and usage guide

test_api.py – Optional local test script

Developed by: Raghad Odwan 
Version: 1.0
Date: [ 1 Nov. 2025]