import pyttsx3

from ConfCustom import config

conf = config ()

voiceoverDir = conf.VoiceOverDir

# TODO : Audio Ducking
def create_voice_over(fileName, text, VoiceID = 0) :
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    engine = pyttsx3.init ()
    voice = engine.getProperty ( 'voices' )  # get the available voices
    engine.setProperty ( 'voice', voice [ VoiceID ].id )  # changing voice to index 1 for female voice
    engine.save_to_file ( text, filePath )
    engine.runAndWait ()
    return filePath


def __SpeakTest(text, VoiceID) :
    engine = pyttsx3.init ()
    voice = engine.getProperty ( 'voices' )  # get the available voices
    # eng.setProperty('voice', voice[0].id) #set the voice to index 0 for male voice
    engine.setProperty ( 'voice', voice [ VoiceID ].id )  # changing voice to index 1 for female voice
    engine.say ( text )
    engine.runAndWait ()


if __name__ == "__main__" :
    ToSay = "Hello and welcome to my youtube channel"
    for i in range(10):
        __SpeakTest(ToSay, i)
        print(i)
