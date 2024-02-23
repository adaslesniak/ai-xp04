import numpy as np
from scipy.spatial.distance import pdist, squareform


class AClusters:

    def __init__(self, with_data:np.array):
        self.original_data = with_data
    

    def _similarity_score(self, some_value:np.ndarray, other_value:np.ndarray):
        raw_differences = some_value - other_value
        squar_differences = np.square(raw_differences)
        return np.sqrt(np.sum(squar_differences)) # this squrt may be little wrong - let's later try without it

    def _prepare_similarity_matrix(self):
        '''it sucks in terms of performace, 
        no parallelism, dobule comupute 
        (adjacency matrix is symetrical, so half calcaulaiton are not needed)
        but it should be all right as proof of concept'''
        adjacency = squareform(pdist(self.original_data, 'euclidean'))
        result = np.zeros_like(adjacency)
        size = adjacency.shape[0]
        for i in range(size):
            for j in range(size):
                result[i, j] = self._similarity_score(adjacency[i], adjacency[j])
        return result
                

    def run(self):
        points_similarity = self._prepare_similarity_matrix()
        return None
    

if __name__ == "__main__":
    import pandas as pd
    data = pd.read_csv('dbscan_dataset.csv').to_numpy()
    x = AClusters(data)
    x.run()
    '''NOTES:
- No, no any custom thershholds. First step is trivial - find biggest value 
in similarity matrix and mark rows that this value represent as having common cluster label. 
Find next highest number and do the same - except if any row belongs to some already defined cluster, 
use this cluster label. 

- That isn't clear. There are 2 questions to solve. 
1 - similarity score should be sum of squared differences or sum of abs differences. 
That is relativity straightforward question and experience in statistics 
says "don't use absolut values".

- Ok. That needs to be experimentally established. Second point is harder if this method 
is to be universal. How to decide if new point belongs to established cluster. 
One idea is my previous description- find nearest neighbor in dataset 
and if it belongs to cluster, add new point to this cluster. But I feel it sucks. 
Find average similarity to all points in this cluster and then check if 
it's still highest value. That feels more robust.

- No - hybrid sucks, It must be "find most similar points in dataset, 
not nearest neighbors of just one point. Find nearest also sucks, 
as one point between two clusters could end up merging those clusters. 
Even worse small movements of one point could change whole visuals. 
If this point is tiny bit closer to next cluster it can be included in that cluster 
and then all other cluster is infected with this cluster, 
while those points are very different. 
A is close to b and b is close to c doesn't mean a is in the same category as c.



- We have similarity score calculated in preprocessing step. Now it's simple. 
Find highest value in table where it doesn't belong to any cluster... (else... ) 
and if highest values connects rows that aren't labeled, create new cluster, 
if other row belongs to cluster, calculated average similarity with 
all points labeled to this cluster. It's not that hard, just find the numbers 
and take average - everything is preprocessed. 
If this there is higher value in table than this average, then proceed with next value... 
it's damn complex computationally and requires a lot of optimization - 
catching similarity to clusters. But that may be way to use one algorithm to rule them all. 
If it would take 12 times as much as k-means but save data scientist from 
running dozens of algorithms with dozens of parameters... it would be breakthrough. 

- There are very computationally demanding methods. Ok. 
One heavy point is preprocessing to get similarity matrix. 
Finding nucleus of first clustler is beyond trivial. 
Now it gets harder as I need cached table that stores (if calculated previously) 
relations between each unassigned point and each defined cluster and between clusters. 
Question. Does this table  need to be updated every time we define new cluster 
or assign new point to a cluster? Yes it must. Then merging is trivial. 
Find next highest value between two unclastered points and in cache table. 
Whichever value is higher, merge clusters (ib both points are clustered) 
or assign point to existing cluster if one point is in cluster and other not, 
finally recalculate cache table for new/changed/merged cluster. 
It is not trivial but not rocket science, can do it. 
If it sucks in efficiency but provides great results someone will pick it up 
and optimize in C++ or something. 

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

- Memory usage. That's just 100 another columns: labels at zoom[0], labels at zoom[1]..
labels at zoom[99]. After iterating thorough next level I can dump it to file, 
so it doesn't cost anything. 

- That's all relatively straight forward. Problem is... 
how to figure out what zoom level 70 means. To calculate if new level was reached.

- From user perspective it should relate to nr of clusters. 
So 1= number of clusters = nr of points, 0 = number of clusters = 1, 
then 0.5 would be nr of clusters = log(0.5 * nr of points). Is that right. 
I want bigger control for small amount if clusters- it differs if there are 3 or 5, 
but lower for high number of clusters. 
Going from 500k clusters to 300k clusters doesn't matter so much.

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

- Continue untill there are only 2 or 1 clusters left. But still I'm not sure.
10% is very small step. For 100k rows how many zoom levels would that be at most? 
0.9 -> 0.9 * 0.9 = 0.81 -> 0.81 * 0.9... 
how many steps till we get to two clusters from 100k rows? 
Remember clamping down. There can't be 33.5 clusters.
103 zoom levels max

- eah. Mostly it would be much lower, as we only store if a) nr of clusters relates 
to new zoom level and b) there was significant change in similarity level used. 
E.g. if similartiy between merged stuff was the same as previously and 
we are at steep curve in reducing number of clusters, no reason to stop and record? 
Or am I little too optimistic and forward looking?
'''