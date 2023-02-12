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

        self.BackgroundMusicDir = self.config ["Audio"] [ "BackgroundMusicDir"]
        self.BackgroundMusicFilePrefix = self.config ["Audio"] ["BackgroundMusicFilePrefix"]
        self.BackgroundMusicCount = self.config ["Audio"] [ "BackgroundMusicCount" ]
        # Photo
        self.screenshotDir = self.config [ "Photo" ] [ "ScreenshotDir" ]
        # Reddit
        self.NumberOfPostsToSelectFrom = self.config [ "Reddit" ] [ "NumberOfPostsToSelectFrom" ]


    def Keys(self) :
        return self.config.keys ()

    def Pairs(self) :
        return self.config.items ()


if __name__ == '__main__' :
    conf = config ()
