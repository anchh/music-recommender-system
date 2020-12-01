# music-recommeder-system
Order of execution:
-> Merge to form data w genres -> something.csv (160k dataset with genres)
-> Cleaning Preoprocessing and forming of the dataset -> onewayoranother2.csv (160k+ MSD w genres and clean) //Later we realise we do not need MSD at all, so we drop it
-> K means from scratch -> Kmeansfromscratch.csv (contains columns for cluster and subcluster as well)
-> PCA f scratch + k means f scratch ->PCAClustering.csv (contains feature values after PCA along with cluster and subcluster value)
-> distance w PCA & clusters using cosine similarity -> gives recommmendations



