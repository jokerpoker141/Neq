import csv
import tempfile
import time

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# THIS IS NOT DONE !!!! work on this more

scopes = [ "https://www.googleapis.com/auth/youtube.readonly" ]
flow = InstalledAppFlow.from_client_secrets_file (
    'client_secrets.json', scopes )

flow.run_local_server ()

tempfile.NamedTemporaryFile ( delete = True )


class YouTubeDataRetriever :
    def __init__(self, api_key) :

        # Creating a youtube object that allows access to the youtube data api v3
        self.video_response = None
        self.video_response = None
        self.youtube = build ( 'youtube', 'v3', developerKey = api_key )

    def search_videos(self, query, max_results=10) :
        # Trying to get the search response from the youtube api and if it fails it will return an empty list
        try :
            search_response = self.youtube.search ().list (
                q = query,
                type = 'video',
                part = 'id,snippet',
                maxResults = max_results
            ).execute ()
            return search_response [ 'items' ]
        except HttpError as e :
            print ( f'An error occurred: {e}' )
            return [ ]

    def get_video_details(self, video_id) :
        try :
            self.video_response = self.youtube.videos ().list (
                id = video_id,
                part = 'snippet,contentDetails,statistics'
            ).execute ()
            return self.video_response [ 'items' ] [ 0 ]
        except HttpError as e :
            print ( f'An error occurred: {e}' )
            return {}

    @staticmethod
    def preprocess_text(text) :
        # implement your text preprocessing code here
        return text

    def get_video_stats(self, video_id) -> dict :

        # declarations
        video_title = None
        video_description = None
        video_duration = None
        video_dimension = None
        video_definition = None
        video_caption = None
        video_projection = None
        video_likes = None
        video_comments = None
        video_views = None
        video_tags = None

        time.sleep ( 1 )
        try :
            self.video_response = self.youtube.videos ().list (
                id = video_id,
                part = 'snippet,contentDetails,statistics'
            ).execute ()

            if debugmode :
                print ( f"self.video_response: {self.video_response}" )
                f = open ( "debug.json", "w", encoding = "UTF-8" )
                f.write ( str ( self.video_response ) )
                f.close ()
            # Extracting required video details from the API response

            video_title = self.video_response [ 'items' ] [ 0 ] [ 'snippet' ] [ 'title' ]
            video_description = self.video_response [ 'items' ] [ 0 ] [ 'snippet' ] [ 'description' ]

            video_duration = self.video_response [ 'items' ] [ 0 ] [ 'contentDetails' ] [ 'duration' ]
            video_dimension = self.video_response [ 'items' ] [ 0 ] [ 'contentDetails' ] [ 'dimension' ]
            video_definition = self.video_response [ 'items' ] [ 0 ] [ 'contentDetails' ] [ 'definition' ]
            video_caption = self.video_response [ 'items' ] [ 0 ] [ 'contentDetails' ] [ 'caption' ]
            video_projection = self.video_response [ 'items' ] [ 0 ] [ 'contentDetails' ] [ 'projection' ]

            video_likes = self.video_response [ 'items' ] [ 0 ] [ 'statistics' ] [ 'likeCount' ]
            video_comments = self.video_response [ 'items' ] [ 0 ] [ 'statistics' ] [ 'commentCount' ]
            video_views = self.video_response [ 'items' ] [ 0 ] [ 'statistics' ] [ 'viewCount' ]
            try :
                video_tags = self.video_response [ 'items' ] [ 0 ] [ 'snippet' ] [ 'tags' ]
            except :
                video_tags = "not found"
                print ( f"No tags found in video {video_id}, {self.video_response}" )
            print ( "tags are " + str ( video_tags ) )
            # Return video details as dictionary
            video_details = {
                'title' : video_title,
                'description' : video_description,
                'duration' : video_duration,
                'likes' : video_likes,
                'comments' : video_comments,
                'tags' : video_tags,
                'dimension' : video_dimension,
                'definition' : video_definition,
                'captions' : video_caption,
                'projection' : video_projection,
                'views' : video_views
            }
            return video_details
        except HttpError as e :
            print ( f'An error occurred: {e}' )
            return {}

    def save_data_to_csv(self, data, csv_path) :
        # there for some random shit I have no idea why it is here but if isn't it stops working
        tempfile.NamedTemporaryFile ( delete = True )
        empty_dict: dict = {}
        header = [ 'Video ID', 'Video Title', 'Video Description', 'Video Duration', 'Video Likes', 'Video Comments',
                   'Video Views', 'Publish Time' ]
        print ( f"data = {data}" )

        with open ( csv_path, 'w', encoding = 'utf-8' ) as f :

            for i in range ( len ( data ) ) :
                print ( f"loop {i}" )
                toWrite = self.get_video_stats ( data [ i ] [ 'id' ] [ 'videoId' ] )
                csv.writer ( f ).writerow ( toWrite.values () )

            if not debugmode :
                writingBuffer: list = [ ]
                csv.DictWriter ( f, fieldnames = header ).writeheader ()
                for video in data :

                    writingBuffer: list = [ ]

                    videoId = video [ "id" ] [ "videoId" ]
                    videoStats: dict = self.get_video_stats ( videoId )
                    if videoStats == empty_dict :
                        print ( "No stats for this video - shit has officially hit the fuckin fan\n"
                                "get ready for sum debuggging" )

                    writingBuffer.append ( video )

                    # 'title': video_title,
                    # 'description': video_description,
                    # 'duration': video_duration,
                    # 'likes': video_likes,
                    # 'comments': video_comments

                    csv.writer ( f ).writerow ( writingBuffer )


if __name__ == '__main__' :
    debugmode = True
    api_key = "AIzaSyDu_7fxxVB8oU4rWTLfDFifT6MVdXbIlGE"
    retriever = YouTubeDataRetriever ( api_key )
    query = 'python programming'
    max_results = 10
    search_results = retriever.search_videos ( query, max_results )
    csv_path = 'data.csv'
    print ( f"search results : {search_results}\n\n type = {type ( search_results )}" )
    retriever.save_data_to_csv ( search_results, csv_path )

if __name__ != '__main__' :
    debugmode = False
    api_key = "AIzaSyDu_7fxxVB8oU4rWTLfDFifT6MVdXbIlGE"
    retriever = YouTubeDataRetriever ( api_key )
    query = 'python programming'
    max_results = 10
    search_results = retriever.search_videos ( query, max_results )
    csv_path = 'data.csv'
    print ( f"{search_results}\nsearch results type = {type ( search_results )}" )
    retriever.save_data_to_csv ( search_results, csv_path )
