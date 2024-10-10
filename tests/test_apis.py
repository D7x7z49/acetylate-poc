import csv
import os
import re
import secrets
import unittest

from dotenv import load_dotenv

from acetylate_poc.targets.api.fofa_api import FofaAPI

load_dotenv()

class TestClassFofaAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.fofa_api_key = os.getenv("FOFA_API_KEY")

    def test_search_all(self):
        fofa = FofaAPI(self.fofa_api_key)
        data = fofa.search_all(
            query=r'product="HFS" && is_honeypot=false && is_domain=true',
            page=1,
            size=10
        )

        print(data)

        self.assertIsInstance(data, (dict, list), "Expected data to be a dictionary or a list.")

    