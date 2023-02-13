from datetime import datetime

from moviepy.editor import AudioFileClip

import voiceover

MAX_WORDS_PER_COMMENT = 100
MIN_COMMENTS_FOR_FINISH = 4
MIN_DURATION = 20
MAX_DURATION = 58


class VideoScript :
    title = ""
    fileName = ""
    titleSCFile = ""
    url = ""
    totalDuration = 0
    frames = [ ]

    def __init__(self, url, title, fileId) -> None :
        self.fileName = f"{datetime.today ().strftime ( '%Y-%m-%d' )}-{fileId}"
        self.url = url
        self.title = title
        self.titleAudioClip = self.__createVoiceOver ( "title", title )

    def canBeFinished(self) -> bool :
        return (len ( self.frames ) > 0) and (self.totalDuration > MIN_DURATION)

    def canQuickFinish(self) -> bool :
        return (len ( self.frames ) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION)

    def addCommentScene(self, text, commentId) -> None :
        wordCount = len ( text.split () )
        if wordCount > MAX_WORDS_PER_COMMENT :
            return True
        frame = ScreenshotScene ( text, commentId )
        frame.audioClip = self.__createVoiceOver ( commentId, text )

        if frame.audioClip == None :
            return True
        self.frames.append ( frame )

    def getDuration(self) :
        return self.totalDuration

    def getFileName(self) :
        return self.fileName

    def getTitle(self) :
        return self.title

    def __createVoiceOver(self, name, text, VoiceType=0, RuntimeChanges=1) :
        # Voice type is a var for the Create_Voice_Over function
        # that determines if the speaker is going to be male or female

        # Runtime changes is a var the question of do you want to change the voice

        # TODO : Add automation settings for RuntimeChanges

        if RuntimeChanges :
            VoiceType = input ( "Voice Type: \n0 - Female \n1 - Male \n\n\n" )
            try :
                VoiceType = int ( VoiceType )
                if not ((VoiceType == 0) or (VoiceType == 1)) :
                    print ( "Please enter 0 or 1" )
                    raise IndexError
            except ValueError :
                print ( "please enter a number" )

        file_path = voiceover.create_voice_over ( f"{self.fileName}-{name}", text, VoiceType )
        audioClip = AudioFileClip ( file_path )
        if self.totalDuration + audioClip.duration > MAX_DURATION :
            print ( "Too high" )
            return None
        self.totalDuration += audioClip.duration
        self.totalDuration
        return audioClip


class ScreenshotScene :
    text = ""
    screenShotFile = ""
    commentId = ""

    def __init__(self, text, commentId) -> None :
        self.text = text
        self.commentId = commentId
