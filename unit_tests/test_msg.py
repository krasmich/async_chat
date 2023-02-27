import json
import unittest

from utils import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, send_message, receive_message


class TestMsg:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def receive(self):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message(self):
        test_socket = TestMsg(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_receive_message(self):
        test_sock_ok = TestMsg(self.test_dict_recv_ok)
        test_sock_err = TestMsg(self.test_dict_recv_err)
        self.assertEqual(receive_message(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(receive_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()