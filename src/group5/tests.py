from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from group5.models import NGram


class NGramApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_ngram_url = reverse('group5:add-ngram')
        self.suggest_word_url = reverse('group5:suggest-word')

        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_ngram_api(self):
        params = {
            'text': 'این یک',
            'dataset': 'fa'
        }
        response = self.client.get(self.suggest_word_url, params)
        self.assertEqual(response.status_code, 200)

        suggestions = response.data['suggestions']
        self.assertNotIn('جمله', suggestions)

        data = {
            'text': 'این یک جمله تست است',
            'dataset_name': 'fa'
        }
        response = self.client.post(self.add_ngram_url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], True)

        response = self.client.get(self.suggest_word_url, params)
        self.assertEqual(response.status_code, 200)
        suggestions = response.data['suggestions']
        self.assertIn('جمله', suggestions)

    def test_add_ngram_api_no_authentication(self):
        self.client.logout()

        data = {
            'text': 'این یک جمله تست است',
            'dataset_name': 'fa'
        }
        response = self.client.post(self.add_ngram_url, data, content_type='application/json')

        self.assertEqual(response.status_code, 403)

    def test_suggest_word_api(self):
        NGram.objects.create(dataset_name='fa', context='این یک', word='جمله', frequency=1)

        params = {
            'text': 'این یک',
            'dataset': 'fa'
        }
        response = self.client.get(self.suggest_word_url, params)
        self.assertEqual(response.status_code, 200)
        suggestions = response.data['suggestions']
        self.assertIn('جمله', suggestions)


if __name__ == '__main__':
    TestCase.main()
