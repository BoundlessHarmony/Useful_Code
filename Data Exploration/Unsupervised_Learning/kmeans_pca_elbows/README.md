# Network Connection Clustering with KMeans and PCA

This script analyzes network connection data using KMeans clustering, with dimensionality reduction provided by Principal Component Analysis (PCA). By clustering the data, we aim to identify patterns or anomalous behaviors in network connections, which can be useful in security analysis and network management. The script includes an Elbow Method visualization to help determine the optimal number of clusters.

## Overview

Network connection logs typically contain high-dimensional data, making direct clustering computationally expensive and potentially ineffective. This script leverages PCA to reduce dimensions, improving clustering performance and making the results more interpretable. The Elbow Method is used to determine the ideal number of clusters.

## Core Concepts

### KMeans Clustering
KMeans is an unsupervised machine learning algorithm that groups data into clusters by minimizing the distance between data points and their assigned cluster centroids. It’s effective for identifying distinct patterns within data.

### Principal Component Analysis (PCA)
PCA is a dimensionality reduction technique that transforms high-dimensional data into a lower-dimensional space by capturing the directions of maximum variance. Reducing dimensions with PCA makes clustering more efficient and often improves cluster separation.

### Elbow Method
The Elbow Method is a heuristic used to select the optimal number of clusters by plotting the "inertia" (sum of squared distances from each point to its centroid) for different cluster counts. The ideal number of clusters is found at the "elbow" point, where adding more clusters provides diminishing returns in reducing inertia.

## Process

1. **Load and Preprocess Data**: Load the network connection data, apply one-hot encoding for categorical columns, convert data to numeric, and fill any missing values.
2. **Standardize Data**: Standardize the data to give each feature equal importance.
3. **Dimensionality Reduction with PCA**: Use PCA to reduce the data to 3 dimensions, retaining the most informative variance.
4. **KMeans Clustering**:
   - Cluster the PCA-transformed data with KMeans, setting an initial number of clusters (e.g., 5).
   - Display the number of points in each cluster.
5. **3D Cluster Visualization**: Plot the clusters in 3D from multiple views (isometric, X, Y, Z views) to observe the cluster structure.
6. **Optimal Cluster Identification with Elbow Method**: Run KMeans with a range of cluster counts and plot the resulting inertia to determine the optimal number of clusters.

## Inputs

- **CSV File**: The script expects a CSV file containing network connection data. The file should have columns such as `timestamp`, `src_ip`, `dst_ip`, `protocol`, and other connection-related fields.
- **Time Range**: Define `start_date` and `end_date` at the top of the script to filter data by time if needed.

## Outputs

- **3D Cluster Plot**: A 3D plot displaying clusters from multiple perspectives.
- **Elbow Plot**: An inertia plot showing how clustering inertia decreases with an increasing number of clusters, helping to select the ideal cluster count.

## Usage

1. **Run the Script**:
   - Load network connection data.
   - The script will preprocess, standardize, reduce dimensions, and apply KMeans clustering.
   - View 3D cluster visualizations and analyze the Elbow Method plot.
2. **Interpret Results**:
   - Review the 3D plots to visually inspect cluster separation.
   - Use the Elbow Method plot to select the optimal number of clusters.

## Example

If clustering 5 groups of network connection data the script might output:

```plaintext
Number of points in cluster 0: 500
Number of points in cluster 1: 450
Number of points in cluster 2: 620
Number of points in cluster 3: 300
Number of points in cluster 4: 700
