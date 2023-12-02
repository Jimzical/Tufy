import json
from googleapiclient.discovery import build
# from youtubeChannelnfo import *
'''
This file contains the functions to get the playlist info
The Fucntions are:
    1. readtxt(filename): reads a text file
    2. view_Json_Format(res): Prints the response in JSON format
    3. getPlaylistVideosIDList(res): Makes a list of Video IDs
    4. getPlaylistVideosIDDict(res): Makes a Dictionary with Title as key and Video ID as value
    5. playlistSelector(playlistID): Selects the playlist Based on the playlist ID
    6. PlaylistSlicedJsonInfo(response): Prints the Sliced JSON info of the playlist
    7. DictPlaylistTitles(response): Prints the Titles of the videos in the playlist
    8. ListPlaylistTitles(response): Prints the Titles of the videos in the playlist
    9. main(): Main Function
'''

def readtxt(filename):
    '''
    --------------------------------------------
    reads a text file
    --------------------------------------------
    params
    @filename: name of the file to be read

    returns
    contents of the file
    '''
    with open(filename, 'r') as f:
        return f.read()



def view_Json_Format(res):
    '''
    --------------------------------------------
    Prints the response in JSON format
    --------------------------------------------
    params
    @res: response from the API
    '''
    # add colors to the JSON output
    import json
    # Print to console
    print(json.dumps(res, indent=4))

def getPlaylistVideosIDList(res):
    '''
    --------------------------------------------
    Makes a list of Video IDs
    --------------------------------------------
    params
    @res: response from the API

    returns
    playlistIdList: list of Video IDs
    '''
    playlistIdList = []

    for item in res['items']:
        playlistIdList.append(item['contentDetails']['videoId'])
    
    return playlistIdList

def getPlaylistVideosIDDict(res):
    '''
    --------------------------------------------
    Makes a Dictionary with Title as key and Video ID as value
    (Not Sure But I think Deleted Videos are not included in the Dictionary Leading to Less Videos in the List Version)
    --------------------------------------------
    params
    @res: response from the API

    returns
    playlistIdDict: Dictionary with Title as key and Video ID as value
    '''
    playlistIdDict = {}

    
    for index in range(len(res['items'])):
        playlistIdDict[res['items'][index]['snippet']['title']] = res['items'][index]['contentDetails']['videoId']
        # playlistIdDict[item['snippet']['title']] = item['contentDetails']['videoId']

    return playlistIdDict


def playlistSelector(playlistID,location = 'info.txt'):
    '''
    --------------------------------------------
    Selects the playlist Based on the playlist ID
    --------------------------------------------

    params
    @playlistID: ID of the playlist

    returns
    response: response object

    UPDATE: Removed the request object from the return
    '''

    api_key = readtxt(location)
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlistID,
        maxResults=50,
    )
    response = request.execute()
    
    newToken = response.get('nextPageToken')
    while newToken:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlistID,
            maxResults=50,
            pageToken=newToken
        )
        response['items'] += request.execute()['items']
        newToken = request.execute().get('nextPageToken')
    
    
    
    
    return response




def PlaylistSlicedJsonInfo(response):
    '''
    --------------------------------------------
    Prints the Sliced JSON info of the playlist
    --------------------------------------------
    params
    @response: response object

    '''
    print('response keys\n',response.keys())
    print('response item keys\n',response['items'][0].keys())
    print('response item snippet keys\n',response['items'][0]['snippet'].keys())

def DictPlaylistTitles(response):
    '''
    --------------------------------------------
    Prints the Titles of the videos in the playlist
    --------------------------------------------
    params
    @response: response object

    '''
    counter = 1
    for key,val in getPlaylistVideosIDDict(response).items():
        print(counter,key,"--------->",val)
        counter += 1
def ListPlaylistTitles(response):
    '''
    --------------------------------------------
    Prints the Titles of the videos in the playlist
    --------------------------------------------
    params
    @response: response object

    '''
    counter = 1
    for i in getPlaylistVideosIDList(response):
        print(counter,i)
        counter += 1

def main(location = 'info.txt'):
    global playlistID

    playlistID = input('Enter the Playlist ID(Basically the PL08xzvm7_udxDvVo6yBFii1rt2W2qtu4V part from the https://www.youtube.com/playlist?list=PL08xzvm7_udxDvVo6yBFii2rt1W2qtu4V): ')
    response = playlistSelector(playlistID,location = location)

    while True:
        option = input('''
        -----------------------------------------------------\n
        Enter the option number
        0. Choose a different Playlist
        1. View JSON Format
        2. View Sliced JSON Info
        3. View List of Video Titles
        4. View Dictionary of Video Titles
        5. View List of Video IDs
        6. View Dictionary of Video IDs
        7. Exit
        -----------------------------------------------------\n
        ''')
        if option == '0':
            playlistID = input('Enter the Playlist ID(Basically the PL08xzvm7_udxDvVo6yBFii1rt2W2qtu4V part from the https://www.youtube.com/playlist?list=PL08xzvm7_udxDvVo6yBFii2rt1W2qtu4V): ')
            response = playlistSelector(playlistID)
        elif option == '1':
            view_Json_Format(response)
        elif option == '2':
            PlaylistSlicedJsonInfo(response)
        elif option == '3':
            ListPlaylistTitles(response)
        elif option == '4':
            DictPlaylistTitles(response)
        elif option == '5':
            print(getPlaylistVideosIDList(response))
        elif option == '6':
            print(getPlaylistVideosIDDict(response))
        elif option == '7':
            break
        else:
            print('Invalid Option')
        
    print(" Thank You for using the program! ")


if __name__ == '__main__':
    main(location = 'info.txt')



    