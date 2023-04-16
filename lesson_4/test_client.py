from unittest import TestCase, main
from time import time
from client import processing_presence, processing_answer


class TestCase(TestCase):

    def test_presence(self):
        message = processing_presence()
        message_new = {
            'action': message['action'],
            'type': message['type'],
            'user': {
                'account_name': message['user']['account_name'],
                'status': message['user']['status']
            }
        }
        self.assertEquals(message_new, {
            'action': 'presence',
            'type': 'status',
            'user': {
                'account_name': 'user0',
                'status': 'I am here!'
        }
    })

    def test_answer_200(self):
        self.assertEquals(processing_answer({
                "response": 200,
                "alert": "OK"
            }), '200 OK')

    def test_answer_400(self):
        self.assertEquals(processing_answer({
            "response": 400,
            "alert": "Bad Request"
        }), '400 Bad Request')

    def test_answer_404(self):
        self.assertEquals(processing_answer({
            "response": 404,
            "alert": "Not Found"
        }), '404 Not Found')

    def test_bad_answer(self):
        self.assertEquals(processing_answer(''), 'Bad server answer')


if __name__ == '__main__':
    main()
