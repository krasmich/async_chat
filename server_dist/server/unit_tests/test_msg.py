import sys


import unittest

sys.path.append('../../../')


class TestSocket:
    def __init__(self, test_dict):
        self.testdict = test_dict

    def send(self, message_to_send):
        json_test_message = json.dumps(self.testdict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def receive(self, max_len):
        json_test_message = json.dumps(self.testdict)
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
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_receive_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(receive_message(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(receive_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
