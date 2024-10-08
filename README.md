# Point Cloud Tree Segmentation and Tree Phenotype Retrieval Program
## Introduction
This project is designed to process tree point cloud data. It offers various essential functionalities, including calculating point cloud density，point cloud segmentation, point cloud merging, and basic phenotype retrieval. Please note that this project is specifically tailored for PLY files. 
### Requirement
Before utilizing this set of code, make sure you have the following packages and libraries installed:
#### open3d: 
You can install it using pip with the following command:
```
pip install open3d
```
#### NumPy:
If you haven't already have NumPy installed, you can install it with:
```
pip install numpy
```
#### scikit-learn (sklearn):
You can install scikit-learn with:
```
pip install scikit-learn
```
ensure that these packages are available in your Python environment before executing the code. Additionally, verify that you have a valid point cloud file located at the specified "file_path" or replace it with the actual path to the point cloud you wish to work with.

## Point Cloud Density Calculation
This python script is designed to  calculates the density of a point cloud by computing the average distance between each point and its nearest neighbor. It also generates a plot illustrating the relationship between the distances to neighbors and the number of points in the point cloud. This visualization helps characterize the sparsity or density of the point cloud.
### Code Explanation
The script loads the point cloud data from the specified file, extracting the relative positions of points in the point cloud，and it applies a radius filter to the point cloud to eliminate noise points.
It achieves this by finding the nearest neighbor for each point, calculating the distance, and then averaging these distances to compute the density of the point cloud.
Finally, it plots the distance distribution of the point cloud, using the distance between each point and its nearest neighbor as the x-axis and the number of points as the y-axis. This visual representation illustrates the density distribution of the point cloud.
### Usage
1. Clone or download this repository to your local machine.
2. Replace all the file path in the code with the path to the point cloud file you want to process,and the location where you wish the file results to be output.
3. Run the script.

## Point Cloud K-Means Clustering Segmentation
This python script is designed to cluster and sort a 3D point cloud using the K-Means clustering algorithm. It utilizes the Open3D library for point cloud processing and the scikit-learn library for K-Means clustering. The code reads a point cloud file, clusters the points based on their color information, and sorts the clusters by the mean color of each cluster.
### Code Explanation
The script loads the point cloud data from the specified file, extracting both colors and points.
K-Means clustering is applied to the colors of the points to group them into clusters.
Each cluster's mean color is calculated, and the clusters are sorted based on this mean color.
The sorted clusters are saved as separate point cloud files.
### Usage
1. Clone or download this repository to your local machine.
2. Replace "file_path" in the code with the path to the point cloud file you want to process.
3. Adjust the n_clusters variable in the K-Means section to set the desired number of clusters.
4. Update the "flie_path" in the code to specify the path where you want to save the resulting point cloud files.
5. Run the script.
## Point Cloud Merging
This code is used to merge point clouds that have been segmented through K-means clustering. It uses the Open3D library to merge multiple PLY format point clouds located in a specified input folder. The merged point cloud is then saved as a single PLY file in the desired output location.
### Code Explanation
This code segment extracts all PLY-format files from the specified target folder. Subsequently, it creates a new point cloud and adds all the point clouds to the newly created one. Finally, it exports the merged point cloud.
### Usage
1. Clone or download this repository to your local machine.
2. Modify the script to specify your input folder and desired output file path:
- Set the `folder_path` variable to the path of the folder containing the PLY files you want to merge.
- Set the `output_path` variable to the path where you want to save the merged point cloud.
3. Run the script.
## Phenotype Retrieval
Intended to measure tree basic phenotype, there are several Python program designed to analyze point cloud data from trees. It provides a set of functionalities to calculate various tree-related phenotype, such as tree height, projection area, undercanopy height, crown breadth and crown maximum radius.
### Code Explanation
This code segment calculates various basic morphological parameters of point cloud trees using custom-defined functions.It calculates the height of trees by sorting the coordinates of the point cloud based on their z-values.Then, It employs a convex hull algorithm to approximate the projected area and then visualizes the convex hull along with the shape of the point cloud, enabling the user to assess its accuracy.It uses a rotation matrix to rotate the point cloud tree at intervals of 1 degree from 0 degrees to 180 degrees. By comparing the diameters measured at each angle, it ultimately determines the maximum diameter of the point cloud tree.Finally, the code will output the values of the aforementioned basic tree morphological 
### Usage
1. Clone or download this repository to your local machine.
2. Load the point cloud data by specifying the file path.
3. Perform point cloud preprocessing, including radius filtering.

## The Measurement of Undercanopy Height
This program achieves the retrieval of advanced parameters under the branches of trees by calculating point clouds the bounding box to approximate and estimate the positions of specific points.
### Code Explanation

This code sorts the tree point cloud file by z-values and then groups every n adjacent points into a group. It calculates the bounding box area for each group of points. By comparing the rate of area expansion, the code identifies the branching point on the tree trunk, recording it as the tree's branch height. Users should adjust the values of n and deta according to their data characteristics to ensure that the number of points in each group and the rate of area expansion match the characteristics of the data being processed. If the appropriate value of deta cannot be determined, users can output the areas of all bounding boxes during code execution to help identify the approximate position of deta based on their changes.
### Usage
1. Clone or download this repository to your local machine.
2. Load the point cloud data by specifying the file path.
3. Set an initial value for "n" and "deta", and adjust it based on the result.
   
## Point Cloud RGB Extration
This program can filter point clouds in a file based on input RGB values by selecting points whose RGB values closely match the specified input.
### Code Explanation
This code first creates a graphical window where the user can input and preview the desired RGB values. Then, it filters the point cloud by selecting points with RGB values where the absolute differences for each component are within 10 of the target values. Afterward, it creates a new point cloud file and outputs the result.
### Usage
1. Clone or download this repository to your local machine.
2. Replace "file_path" in the code with the path to the point cloud file you want to process.
3. Input the RGB value before colsimg the wiondow, the result will be saved in the output file path
