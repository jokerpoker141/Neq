import configparser

from moviepy.audio.fx.volumex import volumex
from moviepy.editor import *
import random
import reddit
import screenshot
import subprocess
import sys
import time
import ConfCustom

# TODO : automatically crop and cut RAW videos for shorts
# TODO : DONE : add background music to the video
# TODO : Add Subscribe to the end of the video
# TODO : Add auto tags
# TODO : Change the video name to the specified video name

conf = ConfCustom.config ()


def createVideo() :
    files = [ ]
    for file in os.listdir ( "BackgroundMusic" ) :
        if file.endswith ( ".mp3" ) :
            files.append ( file )

    config = configparser.ConfigParser ()
    config.read ( 'config.ini' )
    outputDir = config [ "General" ] [ "OutputDirectory" ]

    startTime = time.time ()

    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if len ( sys.argv ) == 2 :
        script = reddit.getContentFromId ( outputDir, sys.argv [ 1 ] )
    else :
        postOptionCount = int ( config [ "Reddit" ] [ "NumberOfPostsToSelectFrom" ] )
        script = reddit.getContent ( outputDir, postOptionCount )
    fileName = script.getFileName ()

    # Create screenshots
    screenshot.getPostScreenshots ( fileName, script )

    # Setup background clip

    bgDir = config [ "General" ] [ "BackgroundDirectory" ]
    bgPrefix = config [ "General" ] [ "BackgroundFilePrefix" ]
    bgCount = int ( config [ "General" ] [ "BackgroundVideos" ] )

    bgIndex = random.randint ( 0, bgCount - 1 )

    #  Ensures that the background directory exists
    while bgIndex < 0 or bgIndex >= bgCount :
        bgIndex = random.randint ( 0, bgCount - 1 )
    try:
        backgroundVideo = VideoFileClip (
            filename = f"{bgDir}/{bgPrefix}{bgIndex}.mp4",
            audio = True ).subclip ( 0, script.getDuration () )
    except :
        backgroundVideo = VideoFileClip (
            filename = f"{bgDir}/{bgPrefix}{bgIndex}.mov",
            audio = True ).subclip ( 0, script.getDuration () )

    w, h = backgroundVideo.size

    def __createClip(screenShotFile, audioClip, marginSize) :  # creates a clip from a screenshot
        imageClip = ImageClip (
            screenShotFile,
            duration = audioClip.duration
        ).set_position ( ("center", "center") )
        imageClip = imageClip.resize ( width = (w - marginSize) )
        videoClip = imageClip.set_audio ( audioClip )
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print ( "Editing clips together..." )
    clips = [ ]
    marginSize = int ( config [ "Video" ] [ "MarginSize" ] )
    clips.append ( __createClip ( script.titleSCFile, script.titleAudioClip, marginSize ) )
    for comment in script.frames :
        clips.append ( __createClip ( comment.screenShotFile, comment.audioClip, marginSize ) )

    # intro
    intro = VideoFileClip("Misc/neq opening.mov")

    # Merge clips into single track
    contentOverlay = concatenate_videoclips ( clips ).set_position ( ("center", "center") )

    # Background Music
    BackgroundMusicFolder = conf.BackgroundMusicDir
    BackgroundMusicName = f"{BackgroundMusicFolder}/{files [ random.randint ( 0, len ( files ) - 1 ) ]}"
    BackgroundMusic = AudioFileClip ( filename = BackgroundMusicName )
    BackgroundMusic = volumex ( BackgroundMusic, 0.25 )

    BackgroundAudio = CompositeAudioClip ( [ BackgroundMusic, contentOverlay.audio ] )

    # Compose background/foreground
    final = CompositeVideoClip (
        clips = [ backgroundVideo, contentOverlay ],
        size = backgroundVideo.size ).set_audio ( BackgroundAudio )  # contentOverlay.audio + BackgroundAudio
    final.duration = script.getDuration ()
    final.set_fps ( backgroundVideo.fps )
    finalDuration = final.subclip ( 0, script.getDuration () )
    tempList : list = [intro, finalDuration ] # if you want to add something to the end in the future use this  #important!
    finalConcat = concatenate_videoclips ( tempList )

    # Write output to file
    print ( "Rendering final video..." )
    bitrate = config [ "Video" ] [ "Bitrate" ]
    threads = config [ "Video" ] [ "Threads" ]
    outputFile = f"{outputDir}/{fileName}.mp4"
    finalConcat.write_videofile (
        outputFile,
        codec = 'mpeg4',
        threads = threads,
        bitrate = bitrate,
    )
    print ( f"Video completed in {time.time () - startTime}" )

    # Preview in VLC for approval before uploading
    if config [ "General" ].getboolean ( "PreviewBeforeUpload" ) :
        vlcPath = config [ "General" ] [ "VLCPath" ]
        p = subprocess.Popen ( [ vlcPath, outputFile ] )
        print ( "Waiting for video review. Type anything to continue" )
        wait = input ()

    print ( "Video is ready to upload!" )
    print ( f"Title: {script.title}  File: {outputFile}" )
    endTime = time.time ()
    print ( f"Total time: {endTime - startTime}" )


if __name__ == "__main__" :
    createVideo ()
