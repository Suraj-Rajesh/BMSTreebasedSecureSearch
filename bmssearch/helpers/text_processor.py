from os import listdir
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer

cached_stopwords = stopwords.words("english")
alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
stemmer = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()

# Remove unicode
def remove_unicode(string):
    try:
        return (bytes(string, "utf-8")).decode('unicode_escape')
    except Exception as details:
        print("Exception in: do_parser.remove_unicode()")
        print(details)
        return "a"

# Process text, extract and tokenize words
def tokenize(text):
    try:
        tokenizer = RegexpTokenizer(r'\w+')
        tokenized_text = " ".join(tokenizer.tokenize(text))
        return tokenized_text.lower()
    except Exception as details:
        print("Exception in: do_parser.tokenize()")
        print(details)

# Remove stopwords from text
def stopwords_remover(text):
    try:
        # Remove unicode from text
#        text.decode('unicode_escape').encode('ascii','ignore')
        parsed_text = ' '.join([word for word in text.split() if word not in cached_stopwords])
        return parsed_text
    except Exception as details:
        print("Exception in: do_parser.stopwords_remover()")
        print(details)

# Remove alphabets
def remove_alphabets(text):
    try:
        parsed_text = ' '.join([word for word in text.split() if word not in alphabets])
        return parsed_text
    except Exception as details:
        print("Exception in: do_parser.remove_alphabets()")
        print(details)
        
# Text to document
def text_to_doc(text, document):
    try:
        with open(document, "w") as file_to_write:
            file_to_write.write(text)
        file_to_write.close()
    except Exception as details:
        print("Exception in: do_parser.text_to_doc()")
        print(details)

# Document to text
def doc_to_text(document):
    try:
        with open(document, "r") as file_to_read:
            text =file_to_read.read()
        file_to_read.close()
        return text
    except Exception as details:
        print("Exception in: do_parser.doc_to_text()")
        print(details)

# Stem text, SnowballStemmer (Porter2)
def stem_text(text):
    try:
        stemmed_text = ' '.join([str(stemmer.stem(word)) for word in text.split()])
        return stemmed_text
    except Exception as details:
        print("Exception in: do_parser.stem_text()")
        print(details)

# Lemmatize text
def lemmatize_text(text):
    try:
        lemmatized_text = ' '.join([str(lemmatizer.lemmatize(word)) for word in text.split()])
        return lemmatized_text
    except Exception as details:
        print("Exception in: do_parser.lemmatize_text()")
        print(details)

# Process raw documents
def prepare_documents(source_directory, destination_directory):
    try:
        files = listdir(source_directory)
        for f in files:
            raw_text = doc_to_text(source_directory + "/" + f)
            cleaned_text = remove_unicode(raw_text)
            tokenized_text = tokenize(cleaned_text)
            stopwords_removed_text = stopwords_remover(tokenized_text)
            processed_text = remove_alphabets(stopwords_removed_text) 
            lemmatized_text = lemmatize_text(processed_text)
            stemmed_text = stem_text(lemmatized_text)
            text_to_doc(stemmed_text, destination_directory + "/" + f)
    except Exception as details:
        print("Exception in: do_parser.prepare_documents")
        print(details)
