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
        self.api_data = sp.playlist(uri, fields=None, market=None, additional_types=('track', ))
        while type(self.api_data) is None:
            self.api_data = sp.playlist(uri, fields=None, market=None, additional_types=('track', ))
        self.uri = uri
        #self.tracks = self.get_track_uris()

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
        #print(type(self.api_data))
        for data in self.api_data['tracks']['items']:
            #print(data)
            try:
                track_list.append(data['track']['uri'])
            except:
                #print(data)
                pass
        return track_list

def create_playlist(name: str, uri):
    playlist = Playlist(uri)
    globals()[name] = playlist
    return globals()[name]

class Playlists_Search:
    def __init__(self, keyword):
        self.api_data_struct = sp.search(keyword, limit=50, offset=0, type='playlist', market='US')
        self.pl_uris = self.get_playlists()

    def get_playlists(self):
        pl_uris = []
        for item in self.api_data_struct['playlists']['items']:
            pl_uris.append(item['uri'])
        return pl_uris
    
    def get_tracks(self):
        tracks = []
        playlists = []
        for pl_uri in self.pl_uris:
            playlist = create_playlist(f"{pl_uri}_pl",pl_uri) #API call per instance
            print(playlist.get_name())
            playlists.append(playlist)
        for pl in playlists:
            tracks.extend(pl.get_track_uris())
        return tracks
        
            
        


def keyword_search(keyword, count):
    if count > 1000:
        offsets = 20
        remainder = 0
    else:
        offsets = int(count/50)
        remainder = count%50
    playlist_uris = []
    call_counter = 0
    pl_counter = 0
    for i in range(offsets):
        results = sp.search(keyword, limit=50, offset=i*50, type='playlist', market='US')
        call_counter += 1
        #print(results)
        for result in results['playlists']['items']:
            playlist_uris.append(result['uri'])
            pl_counter += 1
            #print(result['name'])
            #print(result['uri'])
            #print(result['external_urls'])
            #print('\t' + str(result['owner']['display_name']))
            #print('\t' + str(result['owner']['uri']))
            #print(result)
    if remainder > 0:
        results = sp.search(keyword, limit=remainder, offset=offsets*50, type='playlist', market='US')
        call_counter += 1
        #print(results)
        for result in results['playlists']['items']:
            playlist_uris.append(result['uri'])
            pl_counter += 1
            #print(result['name'])
            #print(result['uri'])
            #print(result['external_urls'])
            #print('\t' + str(result['owner']['display_name']))
            #print('\t' + str(result['owner']['uri']))
            #print(result)
    unique_playlists = list(set(playlist_uris))
    print(f'{count} playlists requested, {len(unique_playlists)} unique playlists found, {call_counter} API calls made')
    return playlist_uris
    
def pl_list_to_track_list(pl_list):
    class_list = []
    track_list = []
    for ind, pl_uri in enumerate(pl_list):
        instance = Playlist(pl_uri)
        class_list.append(instance)
        if ind%50 == 1:
            print(f'{int(100*ind/len(pl_list))}% getting playlist tracks')
    print('playlists converted')
    for playlist in class_list:
        track_list.extend(playlist.get_track_uris())
    return track_list

def sort_list(lst, limit):
    # Create an empty dictionary
    d = {}

    # Iterate through the list and count the number of occurrences of each item
    for item in lst:
        if item in d:
            d[item] += 1
        else:
            d[item] = 1

    # Sort the dictionary by value in descending order
    sorted_d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

    # Return the first "limit" items in the sorted dictionary
    return {k: sorted_d[k] for k in list(sorted_d)[:limit]}

def main():
    """
    # GoodByes: spotify:track:0t3ZvGKlmYmVsDzBJAXK8C
    my_track = Track('spotify:track:0t3ZvGKlmYmVsDzBJAXK8C')
    print(my_track.get_name())
    print(my_track.get_artist_names())
    print(my_track.get_link())
    print(my_track.get_popularity())
    """

    
    my_playlist = Playlist('spotify:playlist:62KyMH162xfRaNpoJnZV8g')
    print(my_playlist.get_name())
    #print(my_playlist.get_uri())
    #print(my_playlist.get_owner_name())
    #print(my_playlist.get_owner_uri())
    #print(my_playlist.get_owner_url())
    #print(my_playlist.get_followers_count())
    print(my_playlist.get_num_tracks())
    print(my_playlist.get_track_uris())
    

    test = Playlists_Search('2Chainz')
    print(test.get_tracks())
    pass



if __name__ == '__main__':
    main()