import logging
import os
from multiprocessing import Pool

from pydub import AudioSegment


def split_mp3(InpFile) :
    print ( "processing: " + InpFile )
    audio = AudioSegment.from_mp3 ( f"RAW/{InpFile}" )
    length = len ( audio )
    clip_length = 58 * 1000  # 58 seconds in milliseconds

    for i in range ( 0, length, clip_length ) :
        start: int = i
        end: int = i + clip_length
        clip = audio [ start :end ]
        clip.export ( f"BackgroundMusic/BGm_Clip_{InpFile}_{str ( round(start + 0.1 / 1000))}_{str ( end / 1000)}.mp3", format = "mp3" )

    print ( f"finished processing: {InpFile}" )


if __name__ == "__main__" :
    files = [ ]
    input_folder = "RAW"
    for file in os.listdir ( input_folder ) :
        if file.endswith ( ".mp3" ) :
            files.append ( file )

    output_folder = "BackgroundMusic"
    logging.basicConfig ( level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )

    logger = logging.getLogger ( __name__ )

    with Pool ( 20 ) as p :
        p.map ( split_mp3, files )
