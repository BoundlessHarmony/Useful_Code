import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# File path configuration
data_file_path = "../data/Day 3/dns.log"

def load_data(file_path):
    """
    Load DNS log data and define column names from the specified row in the file.
    Args:
        file_path (str): Path to the DNS log file.
    Returns:
        pd.DataFrame: DataFrame with initial DNS log data.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        column_names = lines[6].rstrip().split("\t")[1:]

    # Load data and define columns
    df = pd.read_csv(file_path, sep="\t", skiprows=8, names=column_names)
    return df

def clean_data(df):
    """
    Clean the data by removing specific rows, columns, and formatting fields.
    Args:
        df (pd.DataFrame): Raw DNS log DataFrame.
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # df.drop([9999999], inplace=True)  # Drop the last row depending on log format
    df.drop(columns=['ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto'], inplace=True)
    df.drop(columns=['qclass_name', 'qtype_name', 'rcode_name', 'AA', 'TC', 'RD', 'RA', 'Z', 'rejected', 'trans_id', 'rtt'], inplace=True)
    
    # Process 'answers' field to count number of answers
    df['answers'] = df['answers'].str.len()
    
    return df

def sum_TTLs(ttl_string):
    """
    Summarize TTL values from a comma-separated string.
    Args:
        ttl_string (str): Comma-separated TTL values as a string.
    Returns:
        float: Sum of TTL values.
    """
    ttl_values = ttl_string.split(',')
    return np.array(ttl_values, dtype=np.float32).sum()

def apply_transformations(df):
    """
    Apply specific transformations to fields such as TTLs and rcode, and create additional features.
    Args:
        df (pd.DataFrame): DataFrame with DNS log data.
    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    # Replace '-' with '-1' in TTLs and rcode for numerical consistency
    df['TTLs'].replace('-', '-1', inplace=True)
    df['rcode'].replace('-', '-1', inplace=True)
    df['TTLs'] = df['TTLs'].apply(sum_TTLs)  # Sum TTLs
    
    # Create additional features based on the query field
    df['qlength'] = df['query'].apply(len)
    df['qparts'] = df['query'].apply(lambda q: len(q.split('.')))
    df['suffixlength'] = df['query'].apply(lambda q: len(q.split('.')[-1]))
    df['domainlength'] = df['query'].apply(lambda q: len(q.split('.')[-2]) if len(q.split('.')) > 1 else 0)

    return df

def prepare_data_for_modeling(df):
    """
    Prepare the data for clustering by selecting relevant features.
    Args:
        df (pd.DataFrame): DataFrame with DNS log data.
    Returns:
        np.ndarray: NumPy array of selected features.
    """
    selected_columns = ['qtype', 'qlength', 'qparts', 'suffixlength', 'qclass', 'rcode', 'answers', 'TTLs', 'domainlength']
    return df[selected_columns].to_numpy()

def perform_pca(data, n_components=3):
    """
    Reduce dimensionality of the data using PCA.
    Args:
        data (np.ndarray): Scaled data array.
        n_components (int): Number of principal components.
    Returns:
        np.ndarray: Reduced data with specified principal components.
    """
    pca = PCA(n_components)
    return pca.fit_transform(data)

def apply_dbscan_clustering(data, eps=0.8, min_samples=5):
    """
    Apply DBSCAN clustering algorithm to the data.
    Args:
        data (np.ndarray): Scaled data array.
        eps (float): Maximum distance between samples for clustering.
        min_samples (int): Minimum number of samples to form a cluster.
    Returns:
        np.ndarray: Cluster labels.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    return dbscan.fit_predict(data)

def plot_3d_cluster_views(data, labels):
    """
    Display clusters in 3D from multiple views.
    Args:
        data (np.ndarray): Data array with PCA-reduced features.
        labels (np.ndarray): Cluster labels.
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

def display_cluster_samples(df, labels, num_samples=5):
    """
    Display sample rows for each cluster.
    Args:
        df (pd.DataFrame): Original DataFrame with added cluster labels.
        labels (np.ndarray): Cluster labels.
        num_samples (int): Number of sample rows to display per cluster.
    """
    df['cluster'] = labels
    for cluster in np.unique(labels):
        print(f"===========================\nCluster {cluster}\n")
        print(df.loc[df['cluster'] == cluster].head(num_samples))

# Main workflow
df = load_data(data_file_path)
df = clean_data(df)
df = apply_transformations(df)

# Prepare data for clustering
model_data = prepare_data_for_modeling(df)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(model_data)
reduced_data = perform_pca(scaled_data)

# Apply clustering
cluster_labels = apply_dbscan_clustering(scaled_data)

# Plot clusters and display samples
plot_3d_cluster_views(reduced_data, cluster_labels)
display_cluster_samples(df, cluster_labels)
