from text_extraction import PdfTextExtraction
from Chunking import MakeChunks
from collections import Counter
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ------------------- Text Preprocessing -------------------



# Example: 
# Before: ["Hello, world!", "AI is amazing."]
# After: [['hello', 'world'], ['ai', 'is', 'amazing']]



def ChunkTextCleaning(Chunks):
    """Clean text chunks and split into tokens (words)."""
    AllTokens = []
    for Chunk in Chunks:
        Chunk = Chunk.lower().strip()
        for P in [".","?","!",",", ";", ":", "(", ")", "[", "]", "\"", "'"]:
            Chunk = Chunk.replace(P," ")
        tokens = Chunk.split()
        AllTokens.append(tokens)
    return AllTokens






# ------------------- Text Mining Utilities -------------------



# Example: 
# Before: ['the', 'ai', 'is', 'amazing', '!']
# After: ['ai', 'amazing']



STOPWORDS = set([
    "the", "of", "to", "and", "is", "a", "in", "for", "on", "with",
    "by", "an", "be", "are", "as", "at", "this", "that", "from", "or","can","it"
])

def clean_tokens(tokens):
    """Remove stopwords and punctuation."""
    cleaned = []
    for token in tokens:
        token = token.strip(string.punctuation)
        if token and token not in STOPWORDS:
            cleaned.append(token)
    return cleaned

# Example
# {'ai': 2, 'amazing': 1, 'learns': 1, 'fast': 1}


def word_frequency(AllTokens):
    counter = Counter()
    for sentence in AllTokens:
        counter.update(clean_tokens(sentence))
    return counter



#  n=2
# [['ai', 'is', 'amazing'], ['ai', 'learns', 'fast']]
# [('ai', 'is'), ('is', 'amazing'), ('ai', 'learns'), ('learns', 'fast')]

def ngrams(AllTokens, n=2):
    ngram_list = []
    for sentence in AllTokens:
        tokens = clean_tokens(sentence)
        if len(tokens) < n:
            continue
        for i in range(len(tokens)-n+1):
            ngram_list.append(tuple(tokens[i:i+n]))
    return ngram_list

def unique_tokens(AllTokens):
    return set(token for sentence in AllTokens for token in clean_tokens(sentence))

def generate_wordcloud(AllTokens):
    text = " ".join(token for sentence in AllTokens for token in clean_tokens(sentence))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(15,7))
    plt.imshow(wordcloud, interpolation="bicubic")
    plt.axis("off")
    plt.show()

# ------------------- Main Pipeline -------------------

if __name__=="__main__":
    # Step 1: Extract Text
    RawText = PdfTextExtraction("aibook.pdf")
    
    # Step 2: Chunk Text
    Chunks = MakeChunks(RawText)
    
    # Step 3: Clean and tokenize
    AllTokens = ChunkTextCleaning(Chunks)
    
    # Step 4: Text mining directly
    freq = word_frequency(AllTokens)
    print("Top 10 most common words:", freq.most_common(10))
    
    bigrams = ngrams(AllTokens, n=2)
    trigram = ngrams(AllTokens, n=3)
    print("Top 10 bigrams:", Counter(bigrams).most_common(10))
    print("Top 10 trigrams:", Counter(trigram).most_common(10))
    
    print("Total unique tokens:", len(unique_tokens(AllTokens)))
    
    # Step 5: Word cloud
    generate_wordcloud(AllTokens)
