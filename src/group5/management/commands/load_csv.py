from django.core.management.base import BaseCommand

from group5.ngram_utils import NGramModel


class Command(BaseCommand):
    help = 'Load CSV data and generate n-gram model'

    def handle(self, *args, **kwargs):
        ngram_model = NGramModel()
        ngram_model.generate_n_gram_model()
        ngram_model.save_ngram_model()
        ngram_model.load_n_gram_model()
        self.stdout.write(self.style.SUCCESS('N-gram model generated and loaded'))
