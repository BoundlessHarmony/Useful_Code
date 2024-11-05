# DNS Log Data Processing and Clustering

## Overview

This Python script processes DNS log data to identify potential patterns and clusters within the data using machine learning. The main objective is to extract key features from DNS logs, transform and preprocess this data, and perform clustering to group similar DNS requests. This could be useful in analyzing DNS traffic, detecting anomalies, or identifying patterns within the DNS queries.

The script leverages several machine learning techniques:
- **Feature Engineering** to extract relevant details from DNS query data.
- **Data Scaling and Dimensionality Reduction** to standardize and simplify data.
- **Clustering with DBSCAN** to identify groups of similar queries.

## Core Concepts

- **Feature Engineering**: Extracting meaningful features from raw data to make it usable for machine learning.
- **Dimensionality Reduction (PCA)**: Reduces the complexity of high-dimensional data while retaining essential patterns.
- **Clustering (DBSCAN)**: A density-based clustering algorithm that groups points based on the density of neighboring points. It is robust in handling outliers, which may arise in DNS traffic.

## Process Description

1. **Data Loading**: The script reads a DNS log file and defines column names from a specific row in the file.
2. **Data Cleaning**: Unnecessary columns and specific rows are removed to focus on relevant data fields. Some fields are preprocessed to handle missing values or non-numeric data.
3. **Feature Engineering**: Additional features (like query length, number of query parts, suffix length, and domain length) are created based on DNS query information.
4. **Data Scaling**: Using `StandardScaler`, features are standardized for clustering.
5. **Dimensionality Reduction**: PCA (Principal Component Analysis) reduces the data to three dimensions for easier visualization.
6. **Clustering**: DBSCAN groups similar data points, assigning each query to a cluster or labeling it as noise.
7. **Visualization**: The clusters are plotted in 3D from multiple viewpoints for better interpretation.
8. **Cluster Inspection**: The script displays sample rows from each cluster, making it easier to understand cluster composition.

## Inputs

- **DNS Log File**: The script expects a DNS log file located at `../data/Day 3/dns.log`. The file should contain DNS request data with tab-separated values, where each line represents a DNS request and associated metadata.

## Outputs

- **DataFrame with Clustering Labels**: The processed DataFrame includes a new column `cluster`, which holds the assigned cluster label for each DNS request.
- **3D Cluster Plot**: A 3D visualization of the clusters is displayed with multiple viewpoints, allowing for easy inspection of the clusters' structure.
- **Cluster Sample Display**: For each cluster, a sample of rows is displayed in the console for quick inspection.

## Dependencies

- Python 3.x
- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`

## Usage

Run the script as follows:

```bash
python dns_clustering.py
