import pandas as pd

class Filter:

    def __init__(self, songsDf):
        self.userSongsDf = songsDf

    def run(self):
        #calculate number of clusters
        kClusters = max(20, int(self.userSongsDf.shape[0] * 5))

        filename = "K_Classes/" + str(kClusters) + ".csv"
        print("Accesing filename:", filename)
        return self._filter_for_songs(filename)

    def _filter_for_songs(self, filename):
        allSongsDf = pd.read_csv(filename)
        print(allSongsDf.head())
        allSongsDict = dict(zip(allSongsDf.id, allSongsDf.cluster))
        print(allSongsDict)

        filteredList = []

        for index, row in self.userSongsDf.iterrows():
            id = row['spotify_id']
            cluster = allSongsDict[id]

            filtered = allSongsDf[(allSongsDf.cluster == cluster) & (allSongsDf.id != id)]
            filteredList.append(filtered)

        filteredDF = pd.concat(filteredList, ignore_index=True)
        filteredDF = filteredDF.drop_duplicates()
        allIdList = filteredDF['id'].to_list()

        allSongsWithFeaturesDf = pd.read_csv("tracks_features_89338.csv")
        featuresFilteredDf = allSongsWithFeaturesDf[allSongsWithFeaturesDf['id'].isin(allIdList)]

        return featuresFilteredDf













