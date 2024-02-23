import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from a_clusters import AClusters


def read_data(test_set):
    data = pd.read_csv(f'{test_set}_dataset.csv')
    return data.to_numpy()

def apply_dbscan(data, eps=0.3, min_samples=10):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(data)
    return dbscan.labels_

def apply_aclusters(data):
    aclusters = AClusters(data)
    aclusters.run()
    # This is a placeholder for applying your algorithm
    # Replace this with your actual function or class method call
    # For demonstration, let's just return a random clustering
    np.random.seed(42)
    return np.random.randint(0, 2, len(data))

def plot_clusters(data, labels, title):
    # Plotting function to visualize clustering
    plt.figure(figsize=(5, 4))
    unique_labels = np.unique(labels)
    for label in unique_labels:
        # Filter points based on label
        points = data[labels == label]
        plt.scatter(points[:, 0], points[:, 1], label=f"Cluster {label}")
    plt.title(title)
    plt.legend()
    plt.show()

# Main workflow
data = read_data('dbscan')

# Apply DBSCAN
dbscan_labels = apply_dbscan(data)
plot_clusters(data, dbscan_labels, "DBSCAN Clustering")

# Apply AClusters
aclusters_labels = apply_aclusters(data)
plot_clusters(data, aclusters_labels, "AClusters")