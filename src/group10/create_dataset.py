from parsivar import Normalizer, Tokenizer, FindStems
from tqdm import tqdm
from collections import defaultdict
from database_utils import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from database_utils import create_db_connection
from parsivarV2_utils import cleanText, deleteHalfSpace, normalizeVerb, isStopWord
from datasets import load_dataset
import heapq

normalizer = Normalizer()
normalizer_english = Normalizer(pinglish_conversion_needed=True)
tokenizer = Tokenizer()
stemmer = FindStems()


def normalize(text):
    return normalizer.normalize(normalizer_english.normalize(text))


def findStem(tokens, need_stemming=False):
    if need_stemming:
        return [stemmer.convert_to_stem(token) for token in tokens]
    else:
        return tokens


def tokenize(text):
    return tokenizer.tokenize_words(text)


def create_tokens_from_text(text, improve_parsivar):
    text = normalize(text)
    if improve_parsivar:
        text = cleanText(text)
        text = deleteHalfSpace(text)
        text = normalizeVerb(text)
    tokens = tokenize(text)
    stem_tokens = findStem(tokens)
    return stem_tokens


frequency_counter = defaultdict(int)


def count_frequency(tokens):
    for index in range(1, len(tokens)):
        past_word = tokens[index - 1]
        current_word = tokens[index]
        frequency_counter[(past_word, current_word)] += 1


def create_dataset(dataset, improve_parsivar):
    dataset_size = len(dataset["train"])

    for index in tqdm(range(dataset_size), desc="Parsing document"):
        text = dataset["train"][index]["Text"]
        tokens = create_tokens_from_text(text, improve_parsivar)
        count_frequency(tokens)


def merge_dictionaries(normal_probabilities, stopword_probabilities):
    merged_probabilities = defaultdict(list)
    for past_word, entries in normal_probabilities.items():
        merged_probabilities[past_word].extend(entries)

    for past_word, entries in stopword_probabilities.items():
        merged_probabilities[past_word].extend(entries)

    return merged_probabilities


def compute_probabilities(frequency_counter):
    normal_probabilities = defaultdict(list)
    stopword_probabilities = defaultdict(list)

    word_counts = defaultdict(int)

    for (past_word, current_word), count in frequency_counter.items():
        word_counts[past_word] += count

    for (past_word, current_word), count in frequency_counter.items():
        prob = count / word_counts[past_word]
        if isStopWord(current_word):
            heapq.heappush(stopword_probabilities[past_word], (prob, current_word))
            if len(stopword_probabilities[past_word]) > 1:
                heapq.heappop(stopword_probabilities[past_word])
        else:
            heapq.heappush(normal_probabilities[past_word], (prob, current_word))
            if len(normal_probabilities[past_word]) > 2:
                heapq.heappop(normal_probabilities[past_word])

    probabilities = merge_dictionaries(normal_probabilities, stopword_probabilities)
    return probabilities


def save_to_first_database(probabilities):
    mydb = create_db_connection(
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_NAME=DB_NAME,
    )
    cursor = mydb.cursor()
    try:
        cursor.execute("""
                            DROP TABLE IF EXISTS G10_word_probabilities;
                        """)
        mydb.commit()
        print("Table drop successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")

    try:
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS G10_word_probabilities (
                                id INT AUTO_INCREMENT PRIMARY KEY,         
                                past_word TEXT,
                                current_word TEXT,
                                probability REAL
                            )
                        """)
        mydb.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")

    batch_size = 100
    batch = []
    for past_word, top_entries in tqdm(
        probabilities.items(), desc="Processing probabilities"
    ):
        for prob, current_word in top_entries:
            batch.append((past_word, current_word, prob))
            if len(batch) >= batch_size:
                try:
                    cursor.executemany(
                        """
                        INSERT INTO G10_word_probabilities (past_word, current_word, probability)
                        VALUES (%s, %s, %s)
                        """,
                        batch,
                    )
                    mydb.commit()
                except Exception as e:
                    print(f"Batch insert error: {e}")
                batch.clear()

    print("Add probabilities successfully")
    mydb.commit()
    cursor.close()
    mydb.close()


def save_to_second_database(probabilities):
    mydb = create_db_connection(
        DB_HOST=DB_HOST,
        DB_PORT=DB_PORT,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_NAME=DB_NAME,
    )
    cursor = mydb.cursor()
    try:
        cursor.execute("""
                            DROP TABLE IF EXISTS G10_word_probabilities_improve_parsivar;
                        """)
        mydb.commit()
        print("Table drop successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")

    try:
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS G10_word_probabilities_improve_parsivar (
                                id INT AUTO_INCREMENT PRIMARY KEY,         
                                past_word TEXT,
                                current_word TEXT,
                                probability REAL
                            )
                        """)
        mydb.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")

    batch_size = 1000
    batch = []
    for past_word, top_entries in tqdm(
        probabilities.items(), desc="Processing probabilities"
    ):
        for prob, current_word in top_entries:
            batch.append((past_word, current_word, prob))
            if len(batch) >= batch_size:
                try:
                    cursor.executemany(
                        """
                        INSERT INTO G10_word_probabilities_improve_parsivar (past_word, current_word, probability)
                        VALUES (%s, %s, %s)
                        """,
                        batch,
                    )
                    mydb.commit()
                except Exception as e:
                    print(f"Batch insert error: {e}")
                batch.clear()

    print("Add probabilities successfully")
    mydb.commit()
    cursor.close()
    mydb.close()


def save_to_database(probabilities, improve_parsivsar):
    if improve_parsivsar:
        save_to_second_database(probabilities)
    else:
        save_to_first_database(probabilities)


def train_model(improve_parsivar):
    dataset = load_dataset("codersan/Persian-Wikipedia-Corpus")
    create_dataset(dataset, improve_parsivar)
    probabilities = compute_probabilities(frequency_counter)
    save_to_database(probabilities, improve_parsivar)


train_model(improve_parsivar=True)
