# DermAI – Image Validation Module

This repository contains the **image validation and quality-check module** used in the DermAI system.
The module performs a series of **pre-inference checks** to verify whether an uploaded image is suitable for analysis by the skin lesion classification model.

This component is **not a diagnostic model** and does not perform disease detection or classification.

---

## Purpose

The goal of this module is to:

* Filter out invalid or low-quality images
* Prevent unsuitable inputs from reaching the AI classifier
* Improve overall system reliability and user feedback

---

## Validation Checks Implemented

The validation pipeline applies multiple heuristic-based checks:

### 1. File Integrity

* Verifies file existence
* Rejects corrupted or unreadable images

### 2. Resolution Check

* Ensures minimum image resolution requirements are met
* Prevents loss of detail during resizing

### 3. Blur Detection

* Uses Laplacian variance to detect excessive blur
* Rejects images unsuitable for feature extraction

### 4. Skin Area Estimation

* Estimates the proportion of skin pixels using HSV and YCrCb color spaces
* Rejects images with insufficient visible skin region

### 5. Texture Analysis

* Analyzes edge density, texture variance, and grayscale statistics
* Filters images with patterns inconsistent with typical skin textures
* Rejects overly smooth images with no visible lesion-like structures

---

## Output Format

The module returns a structured response containing:

* Validation status (`valid` or `error`)
* Rejection reason (if applicable)
* Human-readable feedback message
* Diagnostic details (e.g., blur score, skin ratio)
* Preprocessed image ready for model inference (for valid inputs)

---

## Role in the DermAI System

This module acts as a **gatekeeper** between user input and the AI classifier.
Only images that pass all validation checks are forwarded to the final classification and explainability stages.

---

## Implementation Notes

* Implemented using OpenCV and NumPy
* Designed to be lightweight and suitable for real-time usage
* Uses heuristic thresholds selected empirically during development

> **Important:**
> This module does **not** guarantee medical validity of images.
> It only evaluates technical suitability for model inference.

---

## File Structure

```
Image-Validation-Module-DermAI/
├── check.py
└── README.md
```

---

## Limitations

* Skin detection relies on color-based heuristics and may fail under extreme lighting conditions
* Thresholds are empirically chosen and may not generalize to all image sources
* This module does not replace clinical image acquisition standards

---

## Developer

**Raghad Mousleh**
AI Engineer

--

احكي 👍
