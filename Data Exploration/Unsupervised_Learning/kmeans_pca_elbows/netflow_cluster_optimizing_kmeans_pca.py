from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ================================
# Function to visualize clusters in 3D from different perspectives

def plot_3d_cluster_views(data, labels):
    """
    Display clusters in 3D from multiple views.
    """
    view_titles = ['Isometric View', 'X-Axis View', 'Y-Axis View', 'Z-Axis View']
    view_elevations = [45, 0, 0, 90]
    view_azimuths = [45, 0, 90, 0]

    fig, axes = plt.subplots(2, 2, figsize=(12, 12), subplot_kw={'projection': '3d'})

    for i, ax in enumerate(axes.flat):
        for cluster_label in np.unique(labels):
            ax.scatter(data[labels == cluster_label, 0], 
                       data[labels == cluster_label, 1], 
                       data[labels == cluster_label, 2], label=f'Cluster {cluster_label}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(view_titles[i])
        ax.view_init(view_elevations[i], view_azimuths[i])

    plt.legend()
    plt.show()

# ================================
# Load and preprocess network connection data

# Define the column names
connection_columns = ['timestamp', 'uid', 'src_ip', 'src_port', 'dst_ip', 'dst_port', 
                      'protocol', 'service', 'duration', 'orig_bytes', 'resp_bytes', 
                      'conn_state', 'local_orig', 'local_resp', 'missed_bytes', 
                      'history', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 
                      'resp_ip_bytes', 'tunnel_parents']

# Load data and parse the timestamp
df_connections = pd.read_csv("<your_file_path>", names=connection_columns, sep='\t', skiprows=8)
df_connections['timestamp'] = pd.to_datetime(df_connections['timestamp'], errors='coerce')

# Drop columns not needed for clustering
df_connections.drop(columns=['src_ip', 'dst_ip', 'timestamp', 'missed_bytes', 'uid', 
                             'service', 'local_orig', 'local_resp', 'tunnel_parents', 
                             'conn_state', 'history'], inplace=True)

# Encode the protocol column and convert all to numeric, filling NaN with 0
df_connections = pd.get_dummies(df_connections, columns=['protocol'], dtype=int)
df_connections = df_connections.apply(pd.to_numeric, errors='coerce').fillna(0)

# ================================
# Standardize and reduce dimensions for clustering

scaler = StandardScaler()
standardized_data = scaler.fit_transform(df_connections)

# Reduce dimensions using PCA to 3 for 3D visualization
pca = PCA(n_components=3)
pca_data = pca.fit_transform(standardized_data)

# ================================
# Apply clustering to PCA-reduced data

kmeans_model = KMeans(n_clusters=5, n_init='auto', random_state=42)
cluster_labels = kmeans_model.fit_predict(pca_data)

# Print the number of points in each cluster
for cluster_id in range(5):
    print(f"Number of points in cluster {cluster_id}: {np.sum(cluster_labels == cluster_id)}")

# Plot 3D views of clustered data
plot_3d_cluster_views(pca_data, cluster_labels)

# ================================
# Function to determine optimal number of clusters using the Elbow Method

def find_optimal_clusters(data, max_clusters=10):
    """
    Determine the optimal number of clusters using the Elbow Method.
    """
    inertia_values = {}
    for num_clusters in range(1, max_clusters):
        kmeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=42)
        kmeans.fit(data)
        inertia_values[num_clusters] = kmeans.inertia_
    
    plt.plot(list(inertia_values.keys()), list(inertia_values.values()), marker='o')
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method for Optimal Clusters")
    plt.show()

    return inertia_values

# Identify the optimal number of clusters for the dataset
cluster_inertia_values = find_optimal_clusters(pca_data, max_clusters=10)
