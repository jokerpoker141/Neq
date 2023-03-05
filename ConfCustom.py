import configparser as cp


# TODO : Improve config parsing

class config :
    def __init__(self, LocationOfConfig=None) :
        if LocationOfConfig is not None :
            print ( "Please specify the location of the config file" )
            exit ( -1 )

        self.config = cp.ConfigParser ()
        self.config.read ( 'config.ini' )

        # General
        self.PreviewBeforeUpload = self.config [ "General" ] [ "PreviewBeforeUpload" ]
        self.VLCPath = self.config [ "General" ] [ "VLCPath" ]
        self.OutputDirectory = self.config [ "General" ] [ "OutputDirectory" ]
        self.BackgroundDirectory = self.config [ "General" ] [ "BackgroundDirectory" ]
        self.BackgroundFilePrefix = self.config [ "General" ] [ "BackgroundFilePrefix" ]
        self.BackgroundVideos = self.config [ "General" ] [ "BackgroundVideos" ]

        # Video
        self.MarginSize = self.config [ "Video" ] [ "MarginSize" ]
        self.Bitrate = self.config [ "Video" ] [ "Bitrate" ]
        self.Threads = self.config [ "Video" ] [ "Threads" ]

        # Audio
        self.VoiceOverDir = self.config [ "Audio" ] [ "VoiceOverDir" ]

        self.BackgroundMusicDir = self.config [ "Audio" ] [ "BackgroundMusicDir" ]
        self.BackgroundMusicFilePrefix = self.config [ "Audio" ] [ "BackgroundMusicFilePrefix" ]
        self.BackgroundMusicCount = self.config [ "Audio" ] [ "BackgroundMusicCount" ]
        # Photo
        self.screenshotDir = self.config [ "Photo" ] [ "ScreenshotDir" ]
        # Reddit
        self.NumberOfPostsToSelectFrom = self.config [ "Reddit" ] [ "NumberOfPostsToSelectFrom" ]

    def PRAW(self) :
        config_ = cp.ConfigParser ()
        config_.read ( 'Praw.ini' )

        conf = {
            "check_for_updates" : config_ [ "DEFAULT" ] [ "check_for_updates" ],

            # Object to kind mappings
            "comment_kind " : config_ [ "DEFAULT" ] [ "comment_kind" ],
            "message_kind" : config_ [ "DEFAULT" ] [ "message_kind" ],
            "redditor_kind" : config_ [ "DEFAULT" ] [ "redditor_kind" ],
            "submission_kind" : config_ [ "DEFAULT" ] [ "submission_kind" ],
            "subreddit_kind" : config_ [ "DEFAULT" ] [ "subreddit_kind" ],
            "trophy_kind" : config_ [ "DEFAULT" ] [ "trophy_kind" ],

            # The URL_general prefix for OAuth-related requests.
            "oauth_url" : config_ [ "DEFAULT" ] [ "oauth_url" ],

            # The amount of seconds of ratelimit to sleep for upon encountering a specific type of 429 error.,
            "ratelimit_seconds" : config_ [ "DEFAULT" ] [ "ratelimit_seconds" ],

            # The URL_general prefix for regular requests.,
            "reddit_url" : config_ [ "DEFAULT" ] [ "reddit_url" ],

            # The URL_general prefix for short URLs.,
            "short_url" : config_ [ "DEFAULT" ] [ "short_url" ],

            # The timeout for requests to Reddit in number of seconds,
            "timeout" : config_ [ "DEFAULT" ] [ "timeout" ],

            "client_id" : "8JANU67KBfzaCTk5yUyboA",
            "client_secret" : "J3Zvhni3fITS9Hh4M3wsESyqcfWwAQ",
            # "user_agent" : "Window10 :BotTestBruh: v0",
            "user_agent" : "Window10:BotTestBruh:v0.1 by u/Fantastic_Snow_5130"
        }
        return conf

    def __Keys(self) :
        return self.config.keys ()

    def __Pairs(self) :
        return self.config.items ()


if __name__ == '__main__' :
    conf = config ()
