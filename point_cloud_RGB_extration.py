import tkinter as tk

# Initialize the rgb_color variable
rgb_color = []

def update_color():
    global rgb_color  # Use the global keyword to declare the variable as a global variable
    try:
        # Get the first set of RGB values entered by the user
        red = int(entry_red.get())
        green = int(entry_green.get())
        blue = int(entry_blue.get())

        # Check if RGB values are in the range of 0 to 255
        if not (0 <= red <= 255) or not (0 <= green <= 255) or not (0 <= blue <= 255) :
            raise ValueError("RGB values must be between 0 and 255")

        # Convert RGB values to hexadecimal representation
        hex_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)


        # Update the background color of the color display labels
        color_label.config(bg=hex_color)

        # Update the global variable rgb_color
        rgb_color = [red, green, blue]

        # Clear error message
        error_label.config(text="")

    except ValueError as e:
        # Handle cases where non-integer or out-of-range values are entered
        color_label.config(bg="gray")

        # Display error message
        error_label.config(text=str(e), fg="red")

def close_window():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("RGB color input")

# Create labels and entry fields for the first set of RGB values
label_red = tk.Label(root, text="red(R):")
label_red.grid(row=0, column=0, padx=10, pady=10)
entry_red = tk.Entry(root)
entry_red.grid(row=0, column=1)

label_green = tk.Label(root, text="green(G):")
label_green.grid(row=1, column=0, padx=10, pady=10)
entry_green = tk.Entry(root)
entry_green.grid(row=1, column=1)

label_blue = tk.Label(root, text="blue(B1):")
label_blue.grid(row=2, column=0, padx=10, pady=10)
entry_blue = tk.Entry(root)
entry_blue.grid(row=2, column=1)


# Create color display labels for the first and second sets
color_label = tk.Label(root, text="color preview", width=30, height=5)
color_label.grid(row=6, columnspan=2, pady=10)

# Create an error message label
error_label = tk.Label(root, text="", fg="red")
error_label.grid(row=8, columnspan=2, pady=5)

# Create the update button
update_button = tk.Button(root, text="update color", command=update_color)
update_button.grid(row=9, columnspan=2, pady=10)

# Create the close button
close_button = tk.Button(root, text="close window", command=close_window)
close_button.grid(row=10, columnspan=2, pady=10)

# Run the main loop
root.mainloop()


import numpy as np
import open3d as o3d


def filter_point_cloud_by_rgb(point_cloud, rgb_range):
    # Get point cloud data
    points = np.asarray(point_cloud.points)

    # Extract color information from the point cloud
    colors = np.clip((np.asarray(point_cloud.colors) * 255).astype(np.uint8), 0, 255)

    # Convert RGB values to wavelengths

    # Get indices within the RGB range
    # Get indices within the RGB range
    filtered_indices = np.where(
        (abs(colors[:, 0] - rgb_range[0]) < 10) &
        (abs(colors[:, 1] - rgb_range[1]) < 10) &
        (abs(colors[:, 2] - rgb_range[2]) < 10)
    )[0]

    # Filter point cloud based on indices
    filtered_points = points[filtered_indices, :]
    filtered_colors = colors[filtered_indices, :]

    # Create a new point cloud object
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    filtered_point_cloud.colors = o3d.utility.Vector3dVector(filtered_colors/255.0)

    return filtered_point_cloud


# Read point cloud data
input_point_cloud_file = r"file_path"
point_cloud = o3d.io.read_point_cloud(input_point_cloud_file)


# Filter the point cloud
filtered_point_cloud = filter_point_cloud_by_rgb(point_cloud, rgb_color)

# Save the filtered point cloud data
output_point_cloud_file = r“file_path"
o3d.io.write_point_cloud(output_point_cloud_file, filtered_point_cloud)
