# Interactive 3D MRI Visualization Toolkit

This Python script is a handy toolkit for visualizing and comparing 3D MRI datasets interactively. Using this, you can explore slices from 3D medical image volumes in axial, sagittal, and coronal planes simultaneously. It even comes with features like overlaying masks, comparing "before" and "after" images, and blending overlays with adjustable transparency. Here’s a quick breakdown of what’s included:

### Features:

1. **Basic Slice Exploration**  
   View slices in all three planes from any 3D array (like an MRI scan). You can scroll through slices interactively!

2. **Mask Overlay with Contours**  
   Visualize regions of interest (e.g., lesions) by overlaying mask contours on MRI slices. Customize the contour thickness too.

3. **Before & After Comparison**  
   Compare two 3D volumes side-by-side (e.g., pre-op and post-op scans) across all three planes. 

4. **Transparent Overlay**  
   Blend an overlay (like a lesion mask) onto the original image with adjustable transparency for better visualisation.

### Why Use It?  
Whether you’re analyzing medical images for research or just exploring MRI datasets, this toolkit lets you quickly inspect and compare 3D data interactively. It’s simple to use and works great for presentations or debugging your preprocessing pipeline!

### Requirements:  
- Python
- `matplotlib`, `SimpleITK`, `cv2`, `numpy`, and `ipywidgets`  
- Works in Jupyter Notebooks for the best interactive experience.

### Acknowledgement
'registration display' is adapted from https://github.com/Angeluz-07
