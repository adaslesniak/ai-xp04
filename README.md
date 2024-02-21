# ai-xp04
Experimental clustering algorithm based on similarity score.

What struck me when I was learning about many clustering algorithms that the were limited to closenses of points, not their similarity. When I thing about clusters rural population isn't part of nearest metropoly. Their common feature is that they are far away from mayor clusters. So negative distance is as important as positive closeness. And this would not only reduce problem of outliers, but make intriguing cluster out of them. There are people who don't like others, who are introverts and stay away and keep only few deep relations. They are very similar even if there is nothing in the data that shows their proximity, as one in free time is watching some science-fiction, other is developing indie-games, third is setting up puzzles. Each of them could replace his hobby and I wouldn't change his essence.

## The plan
Create algorightm that: 
   - standardizes the input data
   - creates adjacency matrix calculating distance between each pair of points
   - creates similarity matrix by comaring distances in two lines (so it's not just distance between those two points, but how similary they are spaced related to everything else)
   - clusters points based on their similarity, not simple closeness

## Initial validation
No sense to put lot of effort into it if it fails to do comparably well what k-means can do while doing comparably well what db-scan can do. That's the measure. If it's not one algo to rull them all, then drop it, makes no sense.

## Furhter plan (if initial validation somehow succeeds)
    - initial version will run untill two clusters are reached, but that's wrong, it's prejudice to assume number of clusters, but it's easy
    - next version will still not use any parameters, but will record significant points and store map of labels for multiple "zoom levels". User may be very interested in detailed granular clustering, or only 2-3 top level clusters... he will have all this processed in one step. Series of results with different zoom level to pick one that is most actionable/explanatory for him.

## Known disadventages
There is quite a lot of calculations, so writing that in Python isn't much more than prototyping, but then prototype is what this project is about, so without further ado...
