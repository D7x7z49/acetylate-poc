import csv
import os
import re
import secrets
import unittest

from dotenv import load_dotenv

from acetylate_poc.targets.apis.fofa_api import FofaAPI
from acetylate_poc.targets.apis.info_api import HostAPI, IpinfoAPI

load_dotenv()


class TestClassFofaAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.FOFA_API_KEY = os.getenv("FOFA_API_KEY")

    def test_search_all(self):
        fofa = FofaAPI(self.FOFA_API_KEY)
        data = fofa.search_all(query=r'product="HFS" && is_honeypot=false && is_domain=true', page=1, size=10)

        print(data)

        self.assertIsInstance(data, (dict, list), "Expected data to be a dictionary or a list.")


class TestClassHostAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.HOST_API_KEY = os.getenv("HOST_API_KEY")

    def test_get_host_info(self):
        host = HostAPI(self.HOST_API_KEY)
        data = host.full_host("google.com")

        print(data)

        self.assertIsInstance(data, (dict, list), "Expected data to be a dictionary or a list.")
