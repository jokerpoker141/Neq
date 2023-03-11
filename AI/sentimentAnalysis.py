import time
from collections import defaultdict
from heapq import nlargest

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob


def timeit(func) :
    def wrapper(*args, **kwargs) :
        start_time = time.time ()
        result = func ( *args, **kwargs )
        end_time = time.time ()
        print ( f"Executed {func.__name__} in {end_time - start_time:.6f} seconds" )
        return result

    return wrapper


def sentimentPolarity() -> dict :
    """
    It takes in a string of text, analyzes it, and returns a dictionary with the sentiment and polarity
    :return: A dictionary with the sentiment and polarity
    """

    # Read input from stdin
    input_text = input ( "Enter your text: " )

    # Perform sentiment analysis
    analysis = TextBlob ( input_text )

    # Determine the sentiment polarity
    if analysis.sentiment.polarity > 0 :
        sentiment = "positive"
    elif analysis.sentiment.polarity == 0 :
        sentiment = "neutral"
    else :
        sentiment = "negative"

    if debugmode :
        print ( analysis.sentiment.polarity )

        # Output the sentiment polarity
        print ( "Sentiment of the input is:", sentiment )

    return {"sentiment" : sentiment, "polarity" : analysis.sentiment.polarity}


# if there are any errors just uncomment these lines and let id download because3 there might be something wrong with
# your install ie. missing install or something like that.
# nltk.download ( 'punkt' )
# nltk.download ( 'stopwords' )

@timeit
def extract_keywords(text, num_keywords) :
    # Tokenize the text into sentences and words
    sentences = sent_tokenize ( text.lower () )
    words = [ word for word in word_tokenize ( text.lower () ) if word.isalpha () ]

    # Remove stop words from the words list
    stop_words = set ( stopwords.words ( 'english' ) )
    words = [ word for word in words if not word in stop_words ]

    # Calculate the word frequency
    word_freq = defaultdict ( int )
    for word in words :
        word_freq [ word ] += 1

    # Calculate the weighted word frequency
    max_freq = max ( word_freq.values () )
    for word in word_freq.keys () :
        word_freq [ word ] /= max_freq

    # Calculate the sentence score using TextRank algorithm
    sentence_score = defaultdict ( int )
    for sentence in sentences :
        for word in word_tokenize ( sentence.lower () ) :
            if word in word_freq.keys () :
                sentence_score [ sentence ] += word_freq [ word ]

    # Get the most important sentences based on their score
    important_sentences = nlargest ( num_keywords, sentence_score, key = sentence_score.get )

    # Extract the keywords from the important sentences
    keywords = [ ]
    for sentence in important_sentences :
        for word in word_tokenize ( sentence.lower () ) :
            if word in word_freq.keys () and word not in stop_words :
                keywords.append ( word )

    return list ( set ( keywords [ :num_keywords ] ) )


# Example usage
text = "Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational " \
       "linguistics concerned with the interactions between computers and human (natural) languages. "

if __name__ == '__main__' :
    # A variable that is used to determine if the program is in debug mode or not.
    debugmode: bool = True
    sentimentPolarity ()
    extract_keywords ( text, 3 )
