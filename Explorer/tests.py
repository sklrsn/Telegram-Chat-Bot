import unittest
from django.test import Client
import json


class ExplorerTestCases(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_exploreByKeyword(self):
        exploreKeywordResponse = self.client.post('http://127.0.0.1:8000/v1/search/exploreByKeyword/',
                                                  json.dumps({"keyword": "Good"}),
                                                  content_type='application/json')
        self.assertEqual(exploreKeywordResponse.status_code, 200)

    def test_exploreByDate(self):
        exploreByDateResponse = self.client.post('http://127.0.0.1:8000/v1/search/exploreByDate/',
                                                 json.dumps({"query_date": "2017/04/09"}),
                                                 content_type='application/json')
        self.assertEqual(exploreByDateResponse.status_code, 200)

    def test_exploreByUserName(self):
        exploreByUserNameResponse = self.client.post('http://127.0.0.1:8000/v1/search/exploreByUserName/',
                                                     json.dumps({"username": ""}),
                                                     content_type='application/json')
        self.assertEqual(exploreByUserNameResponse.status_code, 400)
