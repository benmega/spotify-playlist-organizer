import requests
import json

if __name__ == '__main__':
    # https://developer.spotify.com/documentation/web-api/reference/#category-playlists
    # TODO Update accessCode
    accessCode = 'YOURCODEHERE'  # TODO set this as a parameter of a function

    # sortby = 'danceability' 
    sortby = 'energy' # TODO set this as a parameter of a function
    playlistID = 'PLAYLISTID' # TODO set this as a parameter of a function

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessCode}'
    }

    response = requests.get('https://api.spotify.com/v1/playlists/'+playlistID, headers=headers)

    if not response.status_code == 200:
        print(f'ERROR! Spotify returned status code {response.status_code}')  # TODO make custom error class
    playlistJSON = response.content
    playlistDict = json.loads(playlistJSON)
    tracksDict = playlistDict['tracks']
    trackList = tracksDict['items']
    tracks = []
    for i, song in enumerate(trackList):
        songDetails = json.loads(
            requests.get('https://api.spotify.com/v1/audio-features/' + song['track']['id'], headers=headers).content)
        song[sortby] = songDetails[sortby]
        tracks.append((songDetails[sortby], i))

    tracks.sort(reverse=True)  # the result will be reversed - least danceable to most


    for track in tracks:
        # Change order in playlist
        data = '{"range_start":' + str(track[1]) + ',"insert_before":0,"range_length":1}'
        response = requests.put('https://api.spotify.com/v1/playlists/' + playlistID + '/tracks', headers=headers,
                                data=data)
