from datasets import load_dataset
from parsivar import Normalizer, Tokenizer, FindStems
from tqdm import tqdm
from collections import defaultdict

normalizer = Normalizer()
tokenizer = Tokenizer()
stemmer = FindStems()

def normalize(text):
    return normalizer.normalize(text)

def findStem(tokens):
    return [stemmer.convert_to_stem(token) for token in tokens]

def tokenize(text):
    return tokenizer.tokenize_words(text)

def create_tokens_from_text(text):
    text = normalize(text)
    tokens = tokenize(text)
    stem_tokens = findStem(tokens)
    return stem_tokens

frequency_counter = defaultdict(int)

def count_frequency(tokens):
    for index in range(1, len(tokens)):
        past_word = tokens[index - 1]
        current_word = tokens[index]
        frequency_counter[(past_word, current_word)] += 1

def create_dataset(dataset):
    dataset_size = len(dataset['train'])
    for index in tqdm(range(dataset_size)):
        text = dataset['train'][index]['Text']
        tokens = create_tokens_from_text(text)
        count_frequency(tokens)

dataset = load_dataset("codersan/Persian-Wikipedia-Corpus")
create_dataset(dataset)
print(dict(frequency_counter))
