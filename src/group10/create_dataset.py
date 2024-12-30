from datasets import load_dataset
from parsivar import Normalizer, Tokenizer, FindStems
from tqdm import tqdm
from collections import defaultdict

normalizer = Normalizer()
normalizer_english = Normalizer(pinglish_conversion_needed=True)
tokenizer = Tokenizer()
stemmer = FindStems()

def normalize(text):
    return normalizer.normalize(normalizer_english.normalize(text))

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

def compute_probabilities(frequency_counter):
    probabilities = {}
    word_counts = defaultdict(int)

    for (past_word, current_word), count in frequency_counter.items():
        word_counts[past_word] += count

    for (past_word, current_word), count in frequency_counter.items():
        probabilities[(past_word, current_word)] = count / word_counts[past_word]
    
    return probabilities

def save_to_database(probabilities, db_name="TBA"):
    conn = "TBA"
    cursor = conn.cursor()
    
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS G10_word_probabilities (
                past_word TEXT,
                current_word TEXT,
                probability REAL,
                PRIMARY KEY (past_word, current_word)
            )
        """
        )
    
    for (past_word, current_word), probability in probabilities.items():
        cursor.execute(
        """
            INSERT OR REPLACE INTO G10_word_probabilities (past_word, current_word, probability)
            VALUES (?, ?, ?)
        """, (past_word, current_word, probability))
    
    conn.commit()
    conn.close()


dataset = load_dataset("codersan/Persian-Wikipedia-Corpus")
create_dataset(dataset)
probabilities = compute_probabilities(frequency_counter)
save_to_database(probabilities, )