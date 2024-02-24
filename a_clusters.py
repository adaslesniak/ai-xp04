import numpy as np
from scipy.spatial.distance import pdist, squareform


class AClusters:

    def __init__(self, with_data:np.array):
        self.original_data = with_data
        self.detailed_similarity = None # calculated once, similarity of each pair of points
        self.clustered_similarity = None # recalculated after every step
        self.clusters = None
    

    def _similarity_score(self, some_value:np.ndarray, other_value:np.ndarray):
        raw_differences = some_value - other_value
        squared_differences = np.square(raw_differences)
        return np.sqrt(np.sum(squared_differences)) # TODO: try without sqrt


    def _prepare_similarity_matrix(self):
        """It's very similar to adjacency matrix, except it scores for similarity between points
        Not only distance to other point is stored here, but also it's similarity, how it relates
        to each other point in the data"""
        adjacency = squareform(pdist(self.original_data, 'euclidean'))
        self.detailed_similarity = np.zeros_like(adjacency)
        size = adjacency.shape[0]
        for i in range(size):
            for j in range(size):
                self.detailed_similarity[i, j] = self._similarity_score(adjacency[i], adjacency[j])
            self.detailed_similarity[i, i] = np.inf
        return self.detailed_similarity


    # each point is it's own cluster
    def _prepare_initial_clusters(self):
        self.clustered_similarity = self.detailed_similarity.copy()
        self.clusters = [[i] for i in range(self.detailed_similarity.shape[0])]


    def _most_similar_clusters(self):
        best_match = (0, 0, 0)  #row, index, similarity   
        for i in range(self.clustered_similarity.shape[0]):
            best_for_i = np.argmin(self.clustered_similarity[i])
            best_i_similarity = self.clustered_similarity[i][best_for_i]
            if best_match[2] < best_i_similarity:
                best_match = (i, best_for_i, best_i_similarity)
        return best_match[:2]
    

    def _clusters_similarity(self, cluster_a, cluster_b):
        a_indices = self.clusters[cluster_a] 
        b_indices = self.clusters[cluster_b]
        distances = self.detailed_similarity[np.ix_(a_indices, b_indices)]
        return np.mean(distances)
    

    def _recalculate_clusters_similarity(self, enlarged, dropped):
        """Drop merged, and recalculate similarity scores for column[enlarged] and row[enlarged]
        When two clusters are merged one is removed, the other is changed and it's
        similarity must be recalculated."""
        self.clustered_similarity = np.delete(self.clustered_similarity, dropped, axis=0)  # Remove row
        self.clustered_similarity = np.delete(self.clustered_similarity, dropped, axis=1)  # Remove column
        # once information about cluster that was merged in into other is removed, 
        # we need recalculate scores for enlarged one
        for score_index, score in enumerate(self.clustered_similarity[enlarged]):
            if(score_index == enlarged):
                continue
            self.clustered_similarity[enlarged][score_index] = self._clusters_similarity(enlarged, score_index)
        self.clustered_similarity[:, enlarged] = self.clustered_similarity[enlarged]
        
    
    def _merge_clusters(self, x, y):
        self.clusters[x].extend(self.clusters[y])
        self.clusters.pop(y)


    def _find_clusters(self, how_many):
        print("... calculating clusters")
        while len(self.clusters) > how_many: # change that
            x, y = self._most_similar_clusters()
            self._merge_clusters(x, y)
            self._recalculate_clusters_similarity(x, y)


    def _flatten_clusters(self):
        flattened = []
        for cluster_index, cluster_points in enumerate(self.clusters):
            # Extend the output list with the current index multiplied by the length of the sublist
            flattened.extend([cluster_index] * len(cluster_points))
        return flattened


    def run(self):
        self._prepare_similarity_matrix()
        self._prepare_initial_clusters()
        self._find_clusters(3)
        return self._flatten_clusters()
        
    


# =====================================================
# ================== ugly test run ====================
if __name__ == "__main__":
    import pandas as pd
    test_name = 'start_v2' # beginnings, 
    data = pd.read_csv(f'{test_name}_dataset.csv').to_numpy()
    x = AClusters(data)
    labels = x.run()
    unique_labels = np.unique(labels)
    print(len(unique_labels), 'clusters found after 1st iteration')
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 6))
    for label in unique_labels:
        label_data = data[labels == label]
        plt.scatter(label_data[:, 0], label_data[:, 1], label=f'C_{label}')
        for i, txt in enumerate(np.where(labels == label)[0]):
            plt.annotate(txt, (label_data[i, 0], label_data[i, 1]))
    plt.show()

    

    '''NOTES:

- Find average similarity to all points in this cluster and then check if 
it's still highest value. That feels more robust. It must be "find most similar points in dataset, 
not nearest neighbors of just one point. 

- Find highest value in table where it doesn't belong to any cluster... (else... ) 
and if highest values connects rows that aren't labeled, create new cluster, 
if other row belongs to cluster, calculated average similarity with 
all points labeled to this cluster. It's not that hard, just find the numbers 
and take average - everything is preprocessed. 
If this there is higher value in table than this average, then proceed with next value... 
it requires catching similarity to clusters. 

- I need cached table that stores (if calculated previously) relations between 
each unassigned point and each defined cluster and between clusters. 
Question. Does this table  need to be updated every time we define new cluster 
or assign new point to a cluster? Yes it must. Then merging is trivial. 
Find next highest value between two points and in cache table. 
Whichever value is higher, merge clusters (ib both points are clustered) 
or assign point to existing cluster if one point is in cluster and other not, 
finally recalculate cache table for new/changed/merged cluster. 
It is not trivial but not rocket science, can do it. 



- No any custom thershholds. 

- There is one point I haven't thought through yet. When to stop. 
I want to use this zoom value that is exponential or logarithmic representation of 0 - 
all points are separate clusters, 1 - everything is just one cluster. 
But I want it to be a suggestion- if there are strong similarities, 
continue, if they aren't as strong as before, check for zoom level and stop if reached.

- Hmm - does it make sense? I believe not. It may be even better. 
Determine what zoom level was reached and store values for this zoom level and continue. 
Most of work is already done, user will like to see at different zoom levels and further we go, 
there is exponentially less computation required to finish. 
So calculate and store for zoom values 1-100 and let user get the result he likes most.

- How to figure out what zoom level 70 means. To calculate if new level was reached.

- From user perspective it should relate to nr of clusters. 
So 1= number of clusters = nr of points, 0 = number of clusters = 1, 
then 0.5 would be nr of clusters = log(0.5 * nr of points). Is that right. 
I want bigger control for small amount if clusters- it differs if there are 3 or 5, 
but lower for high number of clusters. 
Going from 500k clusters to 400k clusters doesn't matter so much as going from 7 to 6.

- It's not user controlled. It's calculated. 
User can pick which table of labels he wants to see. 
And there is one think I still don't know. OK. 
Let's say number of zooms is dynamic. 
For data with 10 points there is no way to create 100 zoom level outputs. 
And zoom levels in one data may be 0.1, 0.2, 0.8, 0.95 - 
we detect when things do change, so user doesn't need to go through similar images, 
but has it calculated - only interesting zoom levels are there.

- It will be logarithmic. Each next zoom level is when
    number of unlabeled points + number of clusters is reduced by at least 
    10% from previous zoom level.

- Continue untill there are only 2 or 1 clusters left. 
10% is very small step. For 100k rows how many zoom levels would that be at most? 
0.9 -> 0.9 * 0.9 = 0.81 -> 0.81 * 0.9... 
how many steps till we get to two clusters from 100k rows? 
Remember clamping down. There can't be 33.5 clusters.
103 zoom levels max

- Mostly it would be much lower, as we only store if a) nr of clusters relates 
to new zoom level and b) there was significant change in similarity level used. 
E.g. if similartiy between merged stuff was the same as previously and 
we are at steep curve in reducing number of clusters, no reason to stop and record? 
'''