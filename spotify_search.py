import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

num_playlists = 50

def look_for_playlists(keyword):
    global sp
    global num_playlists

    list_of_playlist_uris = []
    # returns 50 playlists containing the keyword, no idea how it selects the 50 but it is consistent
    for i in range(1):
        results = sp.search(keyword, limit=50, offset=i*50, type='playlist', market=None)
        playlist = results['playlists']
        items = playlist['items']
        for item in items:
            list_of_playlist_uris.append(item['uri'])
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
    
    list_of_playlist_uris = list(set(list_of_playlist_uris))
    num_playlists = len(list_of_playlist_uris)
    print(f'\n{num_playlists} playlists found for keyword {keyword}')
    return list_of_playlist_uris

def find_playlist_track_uris(playlist_uri):
    global sp
    pl_results = sp.playlist(playlist_uri, fields=None, market=None, additional_types=('track', ))
    pl_tracks = pl_results['tracks']
    pl_tracks_items = pl_tracks['items']
    list_of_track_uris = []
    for song in pl_tracks_items:
        song_info = song['track']
        try:
            song_uri = song_info['uri']
        except:
            continue
        list_of_track_uris.append(song_uri)
    return list_of_track_uris

def popular_tracks_based_on_keyword(keyword):
    # get a list of playlist uri's
    playlists = look_for_playlists(keyword)
    track_popularity = {}
    for ind, pl_uri in enumerate(playlists):
        if (ind+1)/len(playlists) == 0:
            pass
        elif ind%25 == 0:
            print(str(round((ind+1)/len(playlists)*100,1)) + '% complete...')
        # get a list of every track uri for each playlist
        track_uris = find_playlist_track_uris(pl_uri)
        for track_uri in track_uris:
            #print(track_uri_to_trackname(track_uri))
            if track_uri in track_popularity:
                #print(str(track_uri_to_trackname(track_uri)) + str(track_popularity[track_uri]) + 'before')
                track_popularity[track_uri] = track_popularity[track_uri] + 1
                if track_popularity[track_uri] >= 4:
                    print(str(track_popularity[track_uri]) + ' : ' + str(track_uri_to_trackname(track_uri)))
                #print(track_popularity[track_uri])
            else:
                track_popularity[track_uri] = 1
        #print('\n\n-----------------------------------\n\n')
    print(f'{len(track_popularity)} unique tracks found')
    
    # sort
    track_popularity_sorted = dict(sorted(track_popularity.items(), key=lambda item: item[1], reverse = True))
    
    # let's get the top 25
    final = {}
    counter = 0
    for key, value in track_popularity_sorted.items():
        final[track_uri_to_trackname(key)] = value
        counter += 1
        if counter == 25:
            break
    #print(f'{len(track_names_and_popularity)} of these tracks are deemed relevant')
    final_sorted = dict(sorted(final.items(), key=lambda item: item[1], reverse = True))
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
