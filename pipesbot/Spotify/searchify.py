import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

class Track:
    def __init__(self, uri: str):
        self.uri = uri
        #self.api_data = sp.track(uri, market=None)
        flag = False
        while(not flag):
            try:
                self.api_data = sp.track(uri, market=None)
                flag = True
            except:
                print('Rate limited. Trying again')
        print(self.api_data['name'])
    
    # construct without an API call
    # playlist_deets['tracks']['items'][0]['track'] passed in

    def get_name(self):
        return self.api_data['name']

    def get_artist_names(self):
        artists = []
        num_times = len(self.api_data['artists'])
        for i in range(num_times):
            artists.append(self.api_data['artists'][i]['name']) 
        return artists
    
    def get_artist_uris(self):
        artists = []
        try:
            for i in range(len(50)): #...because what track has more than 50 artists on it?
                artists.append(self.api_data['artists'][i]['uri']) #...add all artists until we fail
        except:
            pass 
        return artists

    def get_release_date(self):
        return self.api_data['release_date']

    def get_release_date(self):
        return self.api_data['explicit'] == 'True'

    def get_popularity(self):
        "returns an int ([0-100]) of popularity"
        return int(self.api_data['popularity'])

    def get_uri(self):
        return self.api_data['href']

    def get_link(self):
        return self.api_data['external_urls']

class Playlist:
    def __init__(self, uri: str):
        flag = False
        while(not flag):
            try:
                self.api_data = sp.playlist(uri, fields=None, market=None, additional_types=('track', ))
                flag = True
            except:
                print('Rate limited. Trying again')

    # construct without an API call
    # results['playlists']['items'][0] passed in, from the search call

    def get_name(self):
        return self.api_data['name']

    def get_uri(self):
        return self.api_data['uri']

    def get_owner_name(self):
        return self.api_data['owner']['display_name']

    def get_owner_uri(self):
        return self.api_data['owner']['uri']

    def get_owner_url(self):
        return self.api_data['owner']['href']

    def get_followers_count(self):
        return int(self.api_data['followers']['total'])
        
    def get_num_tracks(self):
        return int(len(self.api_data['tracks']['items']))

    def get_track_uris(self):
        track_list = []
        for data in self.api_data['tracks']['items']:
            track_list.append(data['track']['uri'])
        return track_list

class Playlists_Search:
    def __init__(self, keyword):
        self.api_data_struct = sp.search(keyword, limit=50, offset=0, type='playlist', market='US')
        self.pl_uris = self.get_playlists

    def get_playlists(self):
        pl_uris = []
        for i, item in enumerate(self.api_data_struct['playlists']['items']):
            pl_uris.append(item[i]['uri'])
        return pl_uris
    
    def get_tracks(self):
        tracks = []
        playlists = []
        for pl_uri in self.pl_uris:
            flag = False
            while not flag:
                try:
                    playlist = Playlist(f"{pl_uri}_pl",pl_uri) #API call per instance
                    flag = True
                    playlists.append(playlist)
                except:
                    pass
        
            
        




def keyword_search(keyword):
    results = sp.search(keyword, limit=1, offset=0, type='playlist', market='US')
    print(results)
    """
    for result in results['playlists']['items']:
        print(result['name'])
        print(result['external_urls'])
        print('\t' + str(result['owner']['display_name']))
        print('\t' + str(result['owner']['uri']))
        print(result)
    """
    

def main():
    """
    # GoodByes: spotify:track:0t3ZvGKlmYmVsDzBJAXK8C
    my_track = Track('spotify:track:0t3ZvGKlmYmVsDzBJAXK8C')
    print(my_track.get_name())
    print(my_track.get_artist_names())
    print(my_track.get_link())
    print(my_track.get_popularity())
    """

    """
    my_playlist = Playlist('spotify:playlist:62KyMH162xfRaNpoJnZV8g')
    print(my_playlist.get_name())
    print(my_playlist.get_uri())
    print(my_playlist.get_owner_name())
    print(my_playlist.get_owner_uri())
    print(my_playlist.get_owner_url())
    print(my_playlist.get_followers_count())
    print(my_playlist.get_num_tracks())
    print(my_playlist.get_track_uris())
    """

    keyword_search('frat')
    pass



if __name__ == '__main__':
    main()