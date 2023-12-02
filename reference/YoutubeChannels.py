import locale  #to make numbers more readable
import json
from googleapiclient.discovery import build

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

def readableText(number):
    '''
    --------------------------------------------
    makes the number more readable
    --------------------------------------------
    params
    @number: number to be formatted

    returns
    formatted number
    '''
    locale.setlocale(locale.LC_ALL, '')
    # print('Total Views',locale.format_string('%d', int(res['items'][0]['statistics']['viewCount']), grouping=True))
    return locale.format_string('%d', number, grouping=True)

def view_Json_Format(res):
    '''
    --------------------------------------------
    prints the response in JSON format
    --------------------------------------------
    params
    @res: response from the API
    '''
    print(json.dumps(res, indent=4))

def get_channel_id(res):
    '''
    --------------------------------------------
    prints the channel ID
    --------------------------------------------
    params
    @res: response from the API
    '''
    print(res['items'][0]['id'])

def get_channel_title(res):
    '''
    --------------------------------------------
    prints the channel title
    --------------------------------------------
    params
    @res: response from the API

    '''
    print(res['items'][0]['snippet']['title'])

def get_channel_description(res):
    '''
    --------------------------------------------
    prints the channel description
    --------------------------------------------
    params
    @res: response from the API
    '''
    print("working")
    print(res['items'][0]['snippet']['description'])
    if res['items'][0]['snippet']['description'] == '':
        print('No description available')


def get_channel_subscriber_count(res):
    '''
    --------------------------------------------
    prints the channel subscriber count
    --------------------------------------------
    params
    @res: response from the API
    '''

    print('Total Subscribers',readableText(int(res['items'][0]['statistics']['subscriberCount'])))

def get_channel_video_count(res):
    '''
    --------------------------------------------
    prints the channel video count
    --------------------------------------------
    params
    @res: response from the API
    '''

    print('Total Videos',readableText(int(res['items'][0]['statistics']['videoCount'])))

def get_channel_view_count(res):
    '''
    --------------------------------------------
    prints the channel view count
    --------------------------------------------
    params
    @res: response from the API
    '''

    print('Total Views',readableText(int(res['items'][0]['statistics']['viewCount'])))

def get_channel_comment_count(res):
    '''
    # **BROKEN**
    --------------------------------------------
    prints the channel comment count
    --------------------------------------------
    params
    @res: response from the API
    '''

    # print('Total Comments',readableText(int(res['items'][0]['statistics']['commentCount'])))

def get_channel_all(res):
    '''
    --------------------------------------------
    prints all the channel information
    --------------------------------------------
    params
    @res: response from the API
    '''
    get_channel_subscriber_count(res)
    get_channel_video_count(res)
    get_channel_view_count(res)
    # get_channel_comment_count(res)

def main():
    api_key = readtxt(r'info.txt')
    youtube = build('youtube', 'v3', developerKey=api_key)
    # choosing the channel
    channel_username = input('Enter the channel username: ')
    # choose the options
    print('''
    1. Get channel ID
    2. Get channel title
    3. Get channel description
    4. Get channel subscriber count
    5. Get channel video count
    6. Get channel view count
    7. Get channel comment count  (**BROKEN**)
    8. Get all channel information
    9. Get channel information in JSON format
    0. Exit
    ''')
    request  = youtube.channels().list(
        part='statistics',
        forUsername=channel_username
    )

    request_snippet = youtube.channels().list(
        part='snippet',
        forUsername=channel_username
    )
    response = request.execute()
    response_snippet = request_snippet.execute()
    while True:
        option = int(input('Enter the option: '))
        
        match option:
            case 1:
                get_channel_id(response)
            case 2:
                get_channel_title(response_snippet)
            case 3:
                get_channel_description(response_snippet)
            case 4:
                get_channel_subscriber_count(response)
            case 5:
                get_channel_video_count(response)
            case 6:
                get_channel_view_count(response)
            case 7:
                get_channel_comment_count(response)
            case 8:
                get_channel_all(response)
            case 9:
                view_Json_Format(response)
            case 0:
                exit()
            case _:
                try:
                    raise ValueError('Invalid option')
                except ValueError:
                    print('Invalid option')
                
if __name__ == '__main__':
    
    main()
