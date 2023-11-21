def input_wavelength_range():
    # Input the minimum wavelength
    min_wavelength = float(input("Enter the minimum wavelength (unit: nanometers): "))

    # Input the maximum wavelength, ensuring it is greater than the minimum wavelength
    while True:
        max_wavelength = float(input("Enter the maximum wavelength (unit: nanometers, should be greater than the minimum wavelength): "))
        if max_wavelength > min_wavelength:
            break
        else:
            print("Error: The maximum wavelength should be greater than the minimum wavelength. Please enter again.")

    # Return the two variables storing the wavelength range
    return min_wavelength, max_wavelength

# Call the function to obtain the wavelength range and store it in variables
min_wavelength, max_wavelength = input_wavelength_range()

import numpy as np
import open3d as o3d
import colorsys

import colorsys

def rgb_to_wavelength(rgb):
    # Convert RGB to HSV
    hsv = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

    # Calculate wavelength based on a more refined approximation
    # Adjust the coefficients based on your specific use case and requirements
    wavelength = 0.0

    if hsv[0] < 0.1:
        wavelength = 380.0 + hsv[0] * 500.0
    else:
        wavelength = 780.0 - (1.0 - hsv[0]) * 400.0

    return round(wavelength, 3)

def filter_point_cloud_by_rgb(point_cloud, rgb_range):
    # Get point cloud data
    points = np.asarray(point_cloud.points)

    # Extract color information from the point cloud
    colors = (np.asarray(point_cloud.colors) * 255).astype(np.uint8)

    # Convert RGB values to wavelengths
    wavelengths = np.array([rgb_to_wavelength(color) for color in colors])
    filtered_indices = np.where(
        (wavelengths >= wavelength_range[0]) & (wavelengths <= wavelength_range[1])
    )[0]

    # Filter point cloud based on indices
    filtered_points = points[filtered_indices, :]
    filtered_colors = colors[filtered_indices, :]

    # Create a new point cloud object
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors / 255.0)

    return filtered_point_cloud


# Read point cloud data
input_point_cloud_file = r"E:\cloudsegmentation\S-F.ply"
point_cloud = o3d.io.read_point_cloud(input_point_cloud_file)

# Define the RGB range (example range)
wavelength_range = [min_wavelength, max_wavelength]

# Filter the point cloud
filtered_point_cloud = filter_point_cloud_by_rgb(point_cloud, wavelength_range)

# Save the filtered point cloud data
output_point_cloud_file = r"E:\cloudsegmentation\S-F-RGB.ply"
o3d.io.write_point_cloud(output_point_cloud_file, filtered_point_cloud)
