import math
from math import sqrt
from sklearn.neighbors import NearestNeighbors
from scipy.spatial import distance


class PSSA:
    """
        initialize needed parameters
    """

    def __init__(self, preference_df, filtered_df, vector_start, vector_end, playlist_duration=60):
        self.preference_df = preference_df
        self.filtered_df = filtered_df
        self.vector_start = vector_start
        self.vector_end = vector_end
        self.playlist_duration = playlist_duration


    """
        Main PSSA Algorithm
    """
    def run(self):
        myScanLocations = self.Create_Steps()
        
        myPlaylist = []     ### to return to the user
        myArtistlist = []   ### to return to the user
        myGenrelist = []   ### to return to the user
        myIDlist = []       ### to check songs that PSSA returns against the current database, preventing duplicates
        Xlist = []
        Ylist = []
        
        for eachCoordinate in myScanLocations:
            myScanResults = self.Scan(eachCoordinate)
            grabIndex = 0
            foundSong = False
            while foundSong == False:
                if myScanResults.iloc[grabIndex]["id"] in myIDlist:
                    grabIndex += 1
                else:
                    foundSong = True
                    myPlaylist.append(myScanResults.iloc[grabIndex]["name"])
                    myArtistlist.append(myScanResults.iloc[grabIndex]["artist_name"])
                    myGenrelist.append(myScanResults.iloc[grabIndex]["tag_name"])
                    myIDlist.append(myScanResults.iloc[grabIndex]["id"])
                    Xlist.append(myScanResults.iloc[grabIndex]["valence"])
                    Ylist.append(myScanResults.iloc[grabIndex]["energy"])
        
        return [myPlaylist, myArtistlist, myGenrelist, Xlist, Ylist]
                       
        
    def Create_Steps(self):
        point_list = []

        x, y = self.vector_start
        xn, yn = self.vector_end
        n = math.ceil(self.playlist_duration/3.95289333333) ###total playlist time / avg song time = # songs

        point_list.append((x,y)) ### the starting point is the location of the first scan
        x_step = (xn-x)/(n-1)
        y_step = (yn-y)/(n-1)

        for _ in range(n-1):
            x += x_step
            y += y_step
            point_list.append((x,y))

        return point_list
    
    
    def Scan(self, aMoodPoint):
        moodDF = self.filtered_df.copy()
        moodDF = moodDF[["name","tag_name","artist_name","danceability","energy","loudness","speechiness","acousticness","instrumentalness","liveness","valence","tempo","id"]]

        neigh = NearestNeighbors(n_neighbors=15)  ###20 neighbors was chosen do to us imagining that a typical path length
                                                  ### might be 0.5, and if we want a 16-song/1-hour playlist, that's 15 steps
                                                  ### so that is .03 per step. That means we would want a .015 radial distance max
                                                  ### to prevent points from being grabbed multiple times. Most common at n=15.
        neigh.fit(moodDF[["energy", "valence"]]) 

        knn_15_at_i = neigh.kneighbors([aMoodPoint]) ###scan of 15 NN at that mood coordinate point.

        SimilarSongsFromScan = moodDF.iloc[knn_15_at_i[1][0]] #grabs attribute 1, which are the indices of scan. Attr 0 is distances
        feature_distances = []

        for i in range(len(SimilarSongsFromScan)): #this goes through every song that was grabbed in the PSSA scan, for mood similarity
            a = SimilarSongsFromScan.iloc[i]
            aSong_dist_to_User_Selected_songs = []

            for j in range(len(self.preference_df)): #this goes through every song the user selected to compare it to the above
                b = self.preference_df.iloc[j]
                ### forgive me father for this disgusting line of code I have written below
                ### this compares the current song from the scan to every song the user specified by Euclidean feature distance
                ### and adds it to this list of distances. The min is selected since that song is "most like" a user selected song
                aSong_dist_to_User_Selected_songs.append(distance.euclidean([a["danceability"], a["energy"], a["loudness"], a["speechiness"], a["acousticness"], a["instrumentalness"], a["liveness"], a["valence"], a["tempo"]], [b["danceability"], b["energy"], b["loudness"], b["speechiness"], b["acousticness"], b["instrumentalness"], b["liveness"], b["valence"], b["tempo"]]))
            feature_distances.append(min(aSong_dist_to_User_Selected_songs)) 

        SimilarSongsFromScan['feature_dist'] = feature_distances
        SimilarSongsFromScan = SimilarSongsFromScan.sort_values(by=["feature_dist"])
        
        return SimilarSongsFromScan  ### Returns an ordered dataframe based on the song closest to the set of preferences
