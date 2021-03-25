# adapted from https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html#sphx-glr-download-auto-examples-tutorials-run-lda-py

################################################################ TO CHANGE ################################################################
path_json = "/Users/sneha/Desktop/school/comp 767/sample767.jsonl" # path to json file
fields = ["title", "abstract", "authors"] # fields to include in training
path_output = "/Users/sneha/Desktop/school/comp 767" # directory to put graphic output into 
################################################################ TO CHANGE ################################################################

import logging # logs info
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import json # 
import nltk # for preprocessing
#nltk.download('wordnet') # for init download if necessary
from nltk.tokenize import RegexpTokenizer # for tokenization
from nltk.stem.wordnet import WordNetLemmatizer # for lemmatizing
from gensim.models import Phrases # to add sets of adjacent words
from gensim.corpora import Dictionary # to construct dictionary
from gensim.models import LdaModel # to make LDA model
from pprint import pprint # print output in a readable way
import pyLDAvis.gensim

with open(path_json) as fp:
    papers = [json.loads(line) for line in fp.readlines()]

docs = []

for paper in papers:
    cur_paper = ""
    for field in fields:
        if type(paper[field]) is not list and paper[field] is not None:
            cur_paper = cur_paper + paper[field] + " \n"

        elif type(paper[field]) is list and paper[field] is not None:
            for next_field in paper[field]:
                cur_paper = cur_paper + next_field
    
    docs.append(cur_paper)

# format of docs: title \n abstract \n authors \n

# split the docs into tokens
tokenizer = RegexpTokenizer(r'\w+')
for idx in range(len(docs)): # convert to lowercase & split into words
    docs[idx] = docs[idx].lower()  # 
    docs[idx] = tokenizer.tokenize(docs[idx]) 

# take out numbers (but not numbers within words)
docs = [[token for token in doc if not token.isnumeric()] for doc in docs]

# take out words that are one character
docs = [[token for token in doc if len(token) > 1] for doc in docs]

# lemmatize
lemmatizer = WordNetLemmatizer()
docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]

# Add sets of adjacent words if they appear 20+ times (ie "machine learning")
bigram = Phrases(docs, min_count=20)
for idx in range(len(docs)):
    for token in bigram[docs[idx]]:
        if '_' in token:
            docs[idx].append(token)

# constructs word to ID mapping 
dictionary = Dictionary(docs)

# filters out words that occur less than 20 times or are in more than 50% of docs
dictionary.filter_extremes(no_below=20, no_above=0.5)

# transform to vectorized form to put in model
corpus = [dictionary.doc2bow(doc) for doc in docs]

# Finds how many unique tokens we've found and how many docs we have
print('Number of unique tokens: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))

# Set training parameters.
num_topics = 10
chunksize = 2000 # how many docs are processed at a time set to 2000 as default
passes = 20 # how often the model is trained on all the docs set to 20 as default
iterations = 400 # how often do we iterate over each doc set to 400 as default
eval_every = None  # Don't evaluate model perplexity, takes too much time.

# index to word dictionary
temp = dictionary[0] 
id2word = dictionary.id2token

model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)

avg_topic_coherence = sum([t[1] for t in model.top_topics(corpus)]) / num_topics # sum of topic coherences of all topics, divided by the number of topics
print('Average topic coherence: %.4f.' % avg_topic_coherence)
model.print_topics()
visualisation = pyLDAvis.gensim.prepare(model, corpus, dictionary)
full_output_path = path_output + '/LDA_Visualization.html'
pprint(model.print_topics())
pyLDAvis.save_html(visualisation, full_output_path)