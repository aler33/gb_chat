from unittest import TestCase, main
from server import processing_message
from time import time


class TestServer(TestCase):
    def test_no_message(self):
        self.assertEquals (processing_message(''), {
            'response': 400,
            'alert': 'Bad Request'
        })

    def test_bad_request(self):
        self.assertEquals(processing_message({
            "action": "not_presence",
            "time": time(),
            "type": "status",
            "user": {
                "account_name": "user0",
                "status": "I am here!"
            }
        }), {
            'response': 404,
            'alert': 'Not Found'
        })

    def test_good(self):
        self.assertEquals(processing_message({
            "action": "presence",
            "time": time(),
            "type": "status",
            "user": {
                "account_name": "user0",
                "status": "I am here!"
            }
        }), {
            'response': 200,
            'alert': 'OK'
        })


if __name__ == '__main__':
    main()
