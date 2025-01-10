import csv
import os
import re
from collections import defaultdict

from django.conf import settings

from group5.models import NGram


class NGramModel:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NGramModel, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, n=2):
        if not hasattr(self, 'initialized'):
            self.n = n
            self.ngram_model = defaultdict(lambda: defaultdict(int))
            self.initialized = True
            self.model_loaded = False

    def read_phrases_from_csv(self, file_name):
        csv_path = os.path.join(settings.BASE_DIR, 'group5', 'datasets', file_name)
        phrases = []

        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                phrases.append(row[0])

        return phrases

    def normalize_text(self, text):
        text = re.sub(r'[0-9]', '', text)
        text = re.sub(r'[:,\"\'~.<>{}،;()«»]', '', text)
        return text

    def generate_n_gram_model(self):
        datasets_dir = os.path.join(settings.BASE_DIR, 'group5', 'datasets')

        for file_name in os.listdir(datasets_dir):
            dataset_name = os.path.splitext(file_name)[0]
            phrases = self.read_phrases_from_csv(file_name)
            for phrase in phrases:
                self.add_ngram(phrase, dataset_name)

        self.model_loaded = True

    def save_ngram_model(self):
        for (dataset_name, context), word_freq in self.ngram_model.items():
            context_str = ' '.join(context)
            for word, frequency in word_freq.items():
                NGram.objects.create(dataset_name=dataset_name, context=context_str, word=word, frequency=frequency)

    def add_ngram(self, text, dataset_name):
        normalized_phrase = self.normalize_text(text)
        words = normalized_phrase.split()
        for i in range(len(words) - self.n + 1):
            context = tuple(words[i:i + self.n - 1])
            word = words[i + self.n - 1]
            self.ngram_model[(dataset_name, context)][word] += 1
        return True

    # store n-grams in memory
    def load_n_gram_model(self):
        if not self.model_loaded:
            ngrams = NGram.objects.all()
            for ngram in ngrams:
                context = tuple(ngram.context.split())
                self.ngram_model[(ngram.dataset_name, context)][ngram.word] = ngram.frequency
            self.model_loaded = True

    def suggest_word(self, text, dataset_name, n=5):
        self.load_n_gram_model()
        words = text.split()
        if len(words) < 1:
            return ""
        context = tuple(words[-1:])
        suggestions = self.ngram_model.get((dataset_name, context), {})
        if not suggestions:
            return ""
        top_n_values = [t[0] for t in sorted(suggestions.items(), key=lambda item: item[1], reverse=True)[:n]]
        return top_n_values
