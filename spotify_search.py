import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

num_playlists = 50

def look_for_playlists(keyword):
    global sp
    global num_playlists

    list_of_playlist_uris = []
    # returns 50 playlists containing the keyword, no idea how it selects the 50 but it is consistent
    for i in range(19):
        results = sp.search(keyword, limit=50, offset=i*50, type='playlist', market=None)
        """
        playlist = results['playlists']
        items = playlist['items']
        for item in items:
            list_of_playlist_uris.append(item['uri'])
        """
        for result in results['playlists']['items']:
            list_of_playlist_uris.append(result['uri'])
    """
    try:
        #tries to look for more in 50 playlist groups
        for i in range(19):
            results = sp.search(keyword, limit=50, offset=((i+1)*50), type='playlist', market='US')
            playlist = results['playlists']
            items = playlist['items']
            for item in items:
                list_of_playlist_uris.append(item['uri'])
    except:
        print('error occured looking for more playlists')
    """
    
    #list_of_playlist_uris = list(set(list_of_playlist_uris))
    num_playlists = len(list_of_playlist_uris)
    print(f'\n{num_playlists} playlists found for keyword {keyword}')
    return list_of_playlist_uris

def find_playlist_track_uris(playlist_uri):
    global sp
    pl_results = sp.playlist(playlist_uri, fields=None, market=None, additional_types=('track', ))
    list_of_track_uris = []
    for result in pl_results['tracks']['items']:
        try:
            list_of_track_uris.append(result['track']['uri'])
        except:
            continue
    return list_of_track_uris

def popular_tracks_based_on_keyword(keyword):
    t0 = time.time()
    # variables
    track_popularity = {}
    all_tracks = []

    # get a list of playlist uri's
    playlists = look_for_playlists(keyword)

    for ind, pl_uri in enumerate(playlists):
        # status printout
        if (ind+1)/len(playlists) == 0:
            pass
        elif ind%25 == 0:
            print(str(round((ind+1)/len(playlists)*100,1)) + '% complete...')

        # get a list of every track uri for each playlist
        track_uris = find_playlist_track_uris(pl_uri)
        
        for track_uri in track_uris:
            if track_uri in track_popularity:
                track_popularity[track_uri] = track_popularity[track_uri] + 1
            else:
                track_popularity[track_uri] = 1
        """
        # alternate
        all_tracks.extend(track_uris)
        """


    print(f'{len(track_popularity)} unique tracks found')
    """
    # alternate
    all_tracks_once = list(set(all_tracks))
    print(f'{len(all_tracks_once)} unique tracks found')
    """
    
    # sort
    track_popularity_sorted = dict(sorted(track_popularity.items(), key=lambda item: item[1], reverse = True))
    # alternate
    """
    my_dict = {}
    for track in all_tracks_once:
        my_dict[track] = all_tracks.count(track)
    my_dict_sorted = dict(sorted(my_dict.items(), key=lambda item: item[1], reverse = True))
    """
    # let's get the top results
    final = {}

    for key, value in track_popularity_sorted.items():
        if track_uri_to_trackname(key) in final:
            final[track_uri_to_trackname(key)] += value
        else:
            final[track_uri_to_trackname(key)] = value
        if len(final.items()) >= 40:
            break
    #print(f'{len(track_names_and_popularity)} of these tracks are deemed relevant')
    final_sorted = dict(sorted(final.items(), key=lambda item: item[1], reverse = True))
    t1 = time.time()
    print(t1-t0)
    return print_track_dict(final_sorted, keyword)

def track_uri_to_trackname(track_uri):
    global sp
    return sp.track(track_uri, market=None)['name']

def print_track_dict(track_popularity_dict, keyword):
    global num_playlists
    strang = f'\nA spotify playlist search of "{keyword}" found {num_playlists} playlists containing these common songs:'
    count = 1
    count2 = 0
    for key, value in track_popularity_dict.items():
        strang = strang + f'\n{count}. {key} ; ({value})'
        count += 1
    print(len(strang))
    return(strang)

def main():
    popular_tracks_based_on_keyword(input('What keyword should we search with?\n'))

if __name__ == '__main__':
    main()
