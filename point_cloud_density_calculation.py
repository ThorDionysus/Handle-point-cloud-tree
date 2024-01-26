import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import os

# Read point cloud file
pcd = o3d.io.read_point_cloud("input_point_cloud.ply")
# Perform point cloud denoising
pcd, index = pcd.remove_radius_outlier(nb_points=20, radius=0.05)
# Save the denoised file
ply_filename = "output_point_cloud.ply"
# Save point cloud as PLY file
o3d.io.write_point_cloud(ply_filename, pcd)
# Build KD tree to accelerate nearest point search
kdtree = o3d.geometry.KDTreeFlann(pcd)
# Initialize a list to store the nearest neighbor distances for each point
nearest_neighbor_distances = []
# Initialize variables to store the sum and sum of squares of nearest distances
sum_distances = 0.0
sum_distances_squared = 0.0

for i in range(len(pcd.points)):
    [k, idx, _] = kdtree.search_knn_vector_3d(pcd.points[i], 2)  # Find 2 nearest neighbors
    if k == 2:
        nearest_neighbor_distance = np.linalg.norm(pcd.points[i] - pcd.points[idx[1]])
        nearest_neighbor_distances.append(nearest_neighbor_distance)

        # Update the sum and sum of squares of nearest distances
        sum_distances += nearest_neighbor_distance
        sum_distances_squared += nearest_neighbor_distance ** 2
# Calculate the average distance
average_distance = np.mean(nearest_neighbor_distances)
# Calculate distance-weighted value
Q_distance = sum_distances_squared / sum_distances
# Output
print(f"Average nearest neighbor distance: {average_distance:.10f} m")
print(f"Distance-weighted value: {Q_distance:.10f} m")

# Initialize a dictionary to store the count of points for each distance value
distance_count = {}
for i in range(len(pcd.points)):
    [k, idx, _] = kdtree.search_knn_vector_3d(pcd.points[i], 2)  # Find 2 nearest neighbors
    if k == 2:
        nearest_neighbor_distance = round(np.linalg.norm(pcd.points[i] - pcd.points[idx[1]]), 5)

        # Update the count of points for the distance value
        if nearest_neighbor_distance in distance_count:
            distance_count[nearest_neighbor_distance] += 1
        else:
            distance_count[nearest_neighbor_distance] = 1

# Extract distance values and corresponding point counts
distances = list(distance_count.keys())
counts = list(distance_count.values())

# Plot the chart
plt.bar(distances, counts, width=0.0001)  # Adjust width to fit your data range
plt.xlabel('Length')
plt.ylabel('Point Number')
plt.xlim(0, 0.015)

output_folder = "your_png_output_path"
output_filename = "distance_distribution.png"
output_path = os.path.join(output_folder, output_filename)
plt.savefig(output_path)

plt.show()
