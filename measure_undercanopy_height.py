import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

# import point cloud data
pcd = o3d.io.read_point_cloud(r"E:\cloudsegmentation\S-1.ply")
points = np.asarray(pcd.points)
points = points[np.argsort(points[:, 2])]

# Please adjust the value of 'n' based on the actual results
n = 1600  

selected_points = points[:n]
min_x, min_y = np.min(selected_points[:, :2], axis=0)
max_x, max_y = np.max(selected_points[:, :2], axis=0)

lowest_points = points[np.argsort(points[:, 2])[:50]]
avg_lowest_height = np.mean(lowest_points[:, 2])

plt.figure()
plt.scatter(selected_points[:, 0], selected_points[:, 1], c='b', label='Points')
plt.plot([min_x, max_x, max_x, min_x, min_x], [min_y, min_y, max_y, max_y, min_y], c='r', label='Bounding Box')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()
plt.show()

out_of_bounds_point = None
for point in points:
    if np.any(point[:2] < [min_x, min_y]) or np.any(point[:2] > [max_x, max_y]):
        out_of_bounds_point = point
        break

if out_of_bounds_point is not None:
    print("undercanopy_height:", out_of_bounds_point[2]-avg_lowest_height)
