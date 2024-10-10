import csv
import os
import re
import secrets
import unittest

from acetylate_poc.schemas.http_request import RequestsSchema
from acetylate_poc.utils.fetch import extract_file_iterator, separate_file_iterator
from acetylate_poc.utils.requester import AbstractRequester, api_request_handler, api_request_register


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

class TestFunctionFetchFileIterator(unittest.TestCase):

    INFILE = "example/tests/separate_file_iterator_infile.txt"
    OUTFILE = "example/tests/separate_file_iterator_outfile.txt"

    def setUp(self):
        with open(self.INFILE, 'w') as infile:
            infile.write("valid_line_1\n")
            infile.write("invalid_line\n")
            infile.write("valid_line_2\n")
            infile.write("another_invalid_line\n")

    def tearDown(self):
        delete_file(self.INFILE)
        delete_file(self.OUTFILE)

    def test_separate_file_iterator(self):
        regex_pattern = r'^valid_line_\d+$'
        expected_valid_lines = ["valid_line_1", "valid_line_2"]

        valid_lines = list(separate_file_iterator(self.INFILE, self.OUTFILE, regex_pattern))

        self.assertEqual(valid_lines, expected_valid_lines)

        with open(self.OUTFILE, 'r') as outfile:
            invalid_lines = outfile.readlines()
            invalid_lines = [line.strip() for line in invalid_lines]

        self.assertEqual(invalid_lines, ["invalid_line", "another_invalid_line"])

    def test_file_not_found(self):
        regex_pattern = r'^valid_line_\d+$'
        invalid_input_file = "non_existent_file.txt"

        with self.assertRaises(FileNotFoundError):
            list(separate_file_iterator(invalid_input_file, self.OUTFILE, regex_pattern))

    def test_regex_error(self):
        invalid_regex_pattern = r'['

        with self.assertRaises(re.error):
            list(separate_file_iterator(self.INFILE, self.OUTFILE, invalid_regex_pattern))


class TestExtractFileIterator(unittest.TestCase):

    FILE_NDJSON = "example/tests/extract_file_iterator_data.ndjson"
    FILE_CSV = "example/tests/extract_file_iterator_data.csv"

    def setUp(self):
        with open(self.FILE_NDJSON, 'w', encoding='utf-8') as f:
            f.write('{"host": "192.168.1.1", "port": 80}\n')
            f.write('{"host": "192.168.1.2", "port": 443}\n')
        
        with open(self.FILE_CSV, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['host', 'port'])
            writer.writerow(['192.168.1.1', '80'])
            writer.writerow(['192.168.1.2', '443'])

    def tearDown(self):
        delete_file(self.FILE_NDJSON)
        delete_file(self.FILE_CSV)

    def test_extract_ndjson(self):
        filter_keys = ['host']
        results = list(extract_file_iterator(self.FILE_NDJSON, filter_keys))
        expected = [{'host': '192.168.1.1'}, {'host': '192.168.1.2'}]
        self.assertEqual(results, expected)

    def test_extract_csv(self):
        filter_keys = ['host']
        results = list(extract_file_iterator(self.FILE_CSV, filter_keys))
        expected = [{'host': '192.168.1.1'}, {'host': '192.168.1.2'}]
        self.assertEqual(results, expected)


class TestRequester(unittest.TestCase):

    def setUp(self):
        self.url = "https://example.com"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.data = {"key": "value"}

    def test_custom_requester(self):
        # Test custom requester implementation

        @api_request_register("custom_requester")
        class CustomRequester(AbstractRequester):
            def send_request(self, **kwargs):
                method = kwargs.pop('method', None)
                url = kwargs.pop('url', None)
                headers = kwargs.pop('headers', None)
                params = kwargs.pop('params', None)

                print(f"Sending {method} request to {url} with headers {headers} and params {params}.")
                return {"status_code": 200, "content": "Hello, World!"}
            
        @api_request_handler("custom_requester")
        def make_request(method, url, headers, params) -> dict:
            return RequestsSchema(method=method, url=url, headers=headers, params=params)

        response = make_request("GET", self.url, headers=self.headers, params=self.data)

        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["content"], "Hello, World!")