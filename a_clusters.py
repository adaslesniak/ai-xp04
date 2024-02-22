import numpy as np
from scipy.spatial.distance import pdist, squareform


class AClusters:

    def __init__(with_data:np.array):
        self.original_data = with_data
    

    def _similarity_score(some_value:np.ndarray, other_value:np.ndarray):
        raw_differences = some_value - other_value
        squar_differences = np.square(raw_differences)
        return np.sqrt(np.sum(squar_differences))

    def _prepare_similarity_matrix(data:np.array):
        '''it sucks in terms of performace, 
        no parallelism, dobule comupute 
        (adjacency matrix is symetrical, so half calcaulaiton are not needed)
        but it should be all right as proof of concept'''
        adjacency = squareform(pdist(data, 'euclidean'))
        detailed_similarity = np.zeros_like(adjacency)
        for i in range(n):
            for j in range(n):
                detailed_similarity[i, j] = _similarity_score(adjacency[i], adjacency[j])
        return detailed_similarity
                


    

    def run():
        return None