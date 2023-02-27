import json
import unittest

from utils import create_presence, process_server_answer, process_client_message, \
    TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, RESPONSE, ERROR, ENCODING, send_message, receive_message


class TestClient(unittest.TestCase):
    def test_create_presense(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_answer(self):
        self.assertEqual(process_server_answer({RESPONSE: 200}), '200 : OK')

    def test_400_answer(self):
        self.assertEqual(process_server_answer({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_server_answer, {ERROR: 'Bad Request'})


class TestServer(unittest.TestCase):

    err_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        self.assertEqual(process_client_message({TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(process_client_message({ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
