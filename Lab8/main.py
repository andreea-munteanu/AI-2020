from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.manifold import TSNE
from gensim.models import Word2Vec

# nltk.download('stopwords')

file_write = open("p_text.txt", "w")  # here we will write the preprocessed text
# set of english stopwords:
stop_words = set(stopwords.words('english'))


""" _________________________________________ READING TEXT FROM FILE _______________________________________________ """


file_read = open("text.txt", "r")
# extracting .txt content into string
with open("text.txt", "r") as reader:
    data = file_read.read().replace('\n', ' ')


""" _______________________ PREPROCESSING TEXT (tokenize, all lowercase, stopwords) ________________________________ """


def preprocessing(data):
    word_dictionary = {}
    total_words = 0
    # sentence tokenization
    data = sent_tokenize(data)
    # all lowercase:
    for i in range(len(data)):      # i is the index of a sentence
        # all lowercase:
        data[i] = data[i].lower()   # each sentence will be lowercase only
        # removing punctuation
        tokenizer = RegexpTokenizer(r'\w+')
        data[i] = tokenizer.tokenize(data[i])
        # word tokenization:
        for word in data[i]:
            # ignoring stopwords:
            if word not in stop_words and word.isalpha():
                total_words += 1
                if word not in word_dictionary:
                    word_dictionary[word] = 1
                else:
                    word_dictionary[word] += 1
    return word_dictionary, total_words


word_dictionary, total_words = preprocessing(data)
# add them to file_write
file_write.write(str(word_dictionary) + str(total_words))
file_write.write(str(total_words))


""" ____________________________________________ ONE-HOT ENCODING ___________________________________________________"""


dictlist = []
for item in word_dictionary.items():
    temp = [item[0], item[1]]
    dictlist.append(temp)
# print(dictlist)

enc = OneHotEncoder(handle_unknown='ignore')
# dictlist must be something like X = [['Male', 1], ['Female', 3], ['Not specified', 2]] (yes)
enc.fit(dictlist)
dictlist = enc.transform(dictlist).toarray()
print("One-hot encoding:\n", dictlist)


""" ___________________________________________ MOST SIMILAR WORDS __________________________________________________"""

# the list of words for which we want to see the most similar words:
list_to_check = ['war', 'allied', 'force', 'victories', 'jewish']
model = Word2Vec(word_dictionary, min_count=1, size=100, window=5, sg=1)
# size:         The number of dimensions of the embeddings and the default is 100.
# window:       The maximum distance between a target word and words around the target word. The default window is 5.
# min_count:    The minimum count of words to consider when training the model; words
#               with occurrence less than this count will be ignored. The default for min_count is 5.
# workers:      The number of partitions during training and the default workers is 3.
# sg:           The training algorithm, either CBOW(0) or skip gram(1). The default training algorithm is CBOW.
for index in range(len(list_to_check)): # for each word in list_to_check:
    # first, check if word is in vocabulary:
    if list_to_check[index] in word_dictionary:
        model.most_similar(list_to_check[index])

""" ____________________________________________ t-SNE algorithm ____________________________________________________"""


X = np.array(dictlist)
X_embedded = TSNE(n_components=2).fit_transform(X)
Y = X_embedded.shape

