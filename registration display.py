import matplotlib.pyplot as plt
import SimpleITK as sitk
import cv2
import numpy as np
from ipywidgets import interact, FloatSlider, interactive


def explore_3D_array0(arr: np.ndarray, cmap: str = 'gray'):
    """
    Create interactive widget to visualise 3D slices from the 3D array in axial, coronal, and sagittal planes. 

    * arr : 3D array with shape (Z, X, Y) that represents the volume of an MRI image.
    * cmap : Color map to use for plotting slices in matplotlib.pyplot.
    """

    def fn(SLICE):
        # Extract slices for all three planes
        axial_slice = arr[SLICE, :, :]
        coronal_slice = np.flipud(arr[:, SLICE, :])
        sagittal_slice = np.flipud(arr[:, :, SLICE])

        # Display slices side by side
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        axes[0].imshow(axial_slice, cmap=cmap)
        axes[0].axis('off')
        axes[0].set_title(f'Axial Slice {SLICE}')

        axes[1].imshow(coronal_slice, cmap=cmap)
        axes[1].axis('off')
        axes[1].set_title(f'Coronal Slice {SLICE}')

        axes[2].imshow(sagittal_slice, cmap=cmap)
        axes[2].axis('off')
        axes[2].set_title(f'Sagittal Slice {SLICE}')

        plt.tight_layout()
        plt.show()

    # Create the interactive widget with a slice slider
    return interactive(
        fn,
        SLICE=(0, min(arr.shape) - 1) 
    )


def explore_3D_array_with_mask_contour0(arr: np.ndarray, mask: np.ndarray, thickness: int = 1):
    """
    Create interactive widget to visualise 2D slices from the 3D array in axial, coronal, and sagittal planes. 
    Overlay countours of region of interest (cavity and lesion masks)
    
    * arr : 3D array with shape (Z, X, Y) representing the volume (e.g., MRI image).
    * mask : Binary mask with the same shape as `arr`.
    * thickness : Thickness of the contour lines to overlay.
    """
    assert arr.shape == mask.shape, "arr and mask must have the same shape"

    _arr = rescale_linear(arr, 0, 1) 
    _mask = mask.astype(np.uint8)  

    def fn(axial_SLICE, coronal_SLICE, sagittal_SLICE):
        # Extract slices for all three planes
        axial_slice = _arr[axial_SLICE, :, :]
        axial_mask = _mask[axial_SLICE, :, :]

        coronal_slice = np.flipud(_arr[:, coronal_SLICE, :])
        coronal_mask = np.flipud(_mask[:, coronal_SLICE, :])

        sagittal_slice = np.flipud(_arr[:, :, sagittal_SLICE])
        sagittal_mask = np.flipud(_mask[:, :, sagittal_SLICE])

        # Prepare RGB images with contours
        def add_contours(image, mask):
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            return cv2.drawContours(image_rgb, contours, -1, (0, 1, 0), thickness)
               
        axial_contoured = add_contours(axial_slice, axial_mask)
        coronal_contoured = add_contours(coronal_slice, coronal_mask)
        sagittal_contoured = add_contours(sagittal_slice, sagittal_mask)

        # Display images side by side
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        axes[0].imshow(axial_contoured)
        axes[0].axis('off')
        axes[0].set_title(f'Axial Slice {axial_SLICE}')

        axes[1].imshow(coronal_contoured)
        axes[1].axis('off')
        axes[1].set_title(f'Coronal Slice {coronal_SLICE}')

        axes[2].imshow(sagittal_contoured)
        axes[2].axis('off')
        axes[2].set_title(f'Sagittal Slice {sagittal_SLICE}')

        plt.tight_layout()
        plt.show()

    # Create the interactive widget with three slice sliders
    return interactive(
        fn,
        axial_SLICE=(0, arr.shape[0] - 1),
        coronal_SLICE=(0, arr.shape[1] - 1),
        sagittal_SLICE=(0, arr.shape[2] - 1)
    )


def explore_3D_array_comparison0 (arr_before: np.ndarray, arr_after: np.ndarray, cmap: str = 'gray'):
    """
    Create an interactive widget to explore and compare slices across all planes (axial, sagittal, coronal) 
    of 3D arrays representing MRI volumes before and after transformations.

    * arr_before : 3D array with shape (Z, X, Y) that represents the volume of an MRI image, before any transform.
    * arr_after : 3D array with shape (Z, X, Y) that represents the volume of an MRI image, after some transform.
    * cmap : Colormap to use for plotting slices in matplotlib.pyplot.
    """
    assert arr_after.shape == arr_before.shape
    
    def fn(slice_idx: int):
        fig, axes = plt.subplots(3, 2, figsize=(12, 18))
        
        # Axial plane (Z-axis)
        axes[0, 0].imshow(arr_before[slice_idx, :, :], cmap=cmap)
        axes[0, 0].set_title("Axial - Before", fontsize=12)
        axes[0, 1].imshow(arr_after[slice_idx, :, :], cmap=cmap)
        axes[0, 1].set_title("Axial - After", fontsize=12)
        
        # Sagittal plane (X-axis)
        axes[1, 0].imshow(arr_before[:, slice_idx, :], cmap=cmap)
        axes[1, 0].set_title("Sagittal - Before", fontsize=12)
        axes[1, 1].imshow(arr_after[:, slice_idx, :], cmap=cmap)
        axes[1, 1].set_title("Sagittal - After", fontsize=12)
        
        # Coronal plane (Y-axis)
        axes[2, 0].imshow(arr_before[:, :, slice_idx], cmap=cmap)
        axes[2, 0].set_title("Coronal - Before", fontsize=12)
        axes[2, 1].imshow(arr_after[:, :, slice_idx], cmap=cmap)
        axes[2, 1].set_title("Coronal - After", fontsize=12)
        
        # Adjust layout
        for ax in axes.flatten():
            ax.axis("off")
        
        plt.tight_layout()
        plt.show()

    interact(fn, 
             slice_idx=widgets.IntSlider(min=0, max=arr_before.shape[0]-1, step=1, value=0, description='Slice'))


def explore_3D_array_with_transparent_overlay(arr: np.ndarray, overlay: np.ndarray, transparency: float = 0.5):
    """
    The overlay will be superimposed on top of the original array with adjustable transparency.

    * arr : 3D array with shape (Z, X, Y) representing the volume (e.g., MRI image).
    * overlay : 3D array with shape (Z, X, Y) that will be superimposed on `arr`.
    * transparency : float between 0 and 1, where 0 is fully transparent and 1 is fully opaque.
    """
    assert arr.shape == overlay.shape

    _arr = rescale_linear(arr, 0, 1)  
    _overlay = rescale_linear(overlay, 0, 1) 

    def fn(axial_SLICE, coronal_SLICE, sagittal_SLICE, transparency):
        # Extract slices for all three planes
        axial_slice = _arr[axial_SLICE, :, :]
        axial_overlay = _overlay[axial_SLICE, :, :]

        coronal_slice = np.flipud(_arr[:, coronal_SLICE, :])
        coronal_overlay = np.flipud(_overlay[:, coronal_SLICE, :])

        sagittal_slice = np.flipud(_arr[:, :, sagittal_SLICE])
        sagittal_overlay = np.flipud(_overlay[:, :, sagittal_SLICE])

        # Prepare RGB images for display
        def blend_images(base, overlay, transparency):
            base_rgb = cv2.cvtColor(base, cv2.COLOR_GRAY2RGB)
            overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_GRAY2RGB)
            return cv2.addWeighted(base_rgb, 1 - transparency, overlay_rgb, transparency, 0)

        axial_blended = blend_images(axial_slice, axial_overlay, transparency)
        coronal_blended = blend_images(coronal_slice, coronal_overlay, transparency)
        sagittal_blended = blend_images(sagittal_slice, sagittal_overlay, transparency)

        # Display images side by side
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        axes[0].imshow(axial_blended)
        axes[0].axis('off')
        axes[0].set_title(f'Axial Slice {axial_SLICE}')

        axes[1].imshow(coronal_blended)
        axes[1].axis('off')
        axes[1].set_title(f'Coronal Slice {coronal_SLICE}')

        axes[2].imshow(sagittal_blended)
        axes[2].axis('off')
        axes[2].set_title(f'Sagittal Slice {sagittal_SLICE}')

        plt.tight_layout()
        plt.show()

    # Create the interactive widget with three slice sliders and transparency slider
    return interactive(
        fn,
        axial_SLICE=(0, arr.shape[0] - 1),
        coronal_SLICE=(0, arr.shape[1] - 1),
        sagittal_SLICE=(0, arr.shape[2] - 1),
        transparency=FloatSlider(value=transparency, min=0, max=1, step=0.01, description='Transparency:')
    )