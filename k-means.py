import open3d as o3d
import numpy as np
from sklearn.cluster import KMeans

# import point cloud data
point_cloud = o3d.io.read_point_cloud(r"C:\cloudsegmentation\S-F.ply")
colors = np.asarray(point_cloud.colors)
points = np.asarray(point_cloud.points)

# K-Means
kmeans = KMeans(n_clusters=3)  # please change n_cluster 
kmeans.fit(colors)
cluster_labels = kmeans.labels_
cluster_centers = []
for cluster_id in range(max(cluster_labels) + 1):
    cluster_mask = cluster_labels == cluster_id
    cluster_colors = colors[cluster_mask]
    cluster_center = np.mean(cluster_colors, axis=0)
    cluster_centers.append(cluster_center)

sorted_cluster_indices = np.argsort(cluster_centers, axis=0)[:, 0]  # 根据R通道的值排序

sorted_point_clouds = [o3d.geometry.PointCloud() for _ in range(len(cluster_centers))]

for sorted_cluster_id, original_cluster_id in enumerate(sorted_cluster_indices):
    cluster_mask = cluster_labels == original_cluster_id
    sorted_cluster_colors = colors[cluster_mask]
    sorted_cluster_points = points[cluster_mask]

    sorted_point_cloud = o3d.geometry.PointCloud()
    sorted_point_cloud.colors = o3d.utility.Vector3dVector(sorted_cluster_colors)
    sorted_point_cloud.points = o3d.utility.Vector3dVector(sorted_cluster_points)
    sorted_point_clouds[sorted_cluster_id] = sorted_point_cloud

for sorted_cluster_id, sorted_cluster_point_cloud in enumerate(sorted_point_clouds):
    o3d.io.write_point_cloud(f"C:\cloudsegmentation\S-KMeans-Sorted{sorted_cluster_id}.ply", sorted_cluster_point_cloud)
