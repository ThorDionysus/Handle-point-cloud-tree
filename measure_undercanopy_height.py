import open3d as o3d
import numpy as np

# Read point cloud data
pcd = o3d.io.read_point_cloud(r"your-point-cloud-flie.ply")

# Convert point cloud to NumPy array
points = np.asarray(pcd.points)
points = points[np.argsort(points[:, 2])]

# Define n, representing the number of points to compare
n = 1000  # You can adjust the value of n as needed
deta = 0.5

def split_array(arr, n):
    arr = np.asarray(arr)
    num_groups = int(np.ceil(len(arr) / n))
    groups = [arr[i * n:(i + 1) * n] for i in range(num_groups)]
    return groups

def compute_bounding_box_area(group):
    min_bound = np.min(group, axis=0)
    max_bound = np.max(group, axis=0)
    # Calculate length and width
    length = max_bound[0] - min_bound[0]
    width = max_bound[1] - min_bound[1]
    # Calculate area
    area = length * width
    return area

result = split_array(points, n)
areas = []  # Initialize a list to store the area of each bounding box

for i, group in enumerate(result):
    area = compute_bounding_box_area(group)
    areas.append(area)
# Print the area of each bounding box
#for i, area in enumerate(areas):
    #print(f"Area of Bounding Box for Group {i+1}: {area}")

stop_index = None
for i in range(1, len(areas)):
    average_value = np.mean(areas[:i])
    abs_diff = abs(areas[i] - average_value)

    if abs_diff / average_value > deta:
        stop_index = i
        break

if stop_index is not None:
    print(f"Stopping index: {stop_index}")
    points_z_avg_first_20 = np.mean(points[:20, 2])

    # Calculate the average z value for group(stop_index)
    group_z_avg_stop_index = np.mean(result[stop_index+1][:20, 2])

    # Calculate the difference between the two average z values
    z_avg_diff = group_z_avg_stop_index - points_z_avg_first_20
    print(f"undercanopy height: {z_avg_diff}")
else:
    print("No significant difference found.")
