from elkme import elks
import unittest

NULROUTE = '+46700000000'

class TestNumberValidation(unittest.TestCase):
    ec = elks.Elks()

    def test_nulroute(self):
        self.assertTrue(self.ec.validate_number(NULROUTE))

    def test_empty(self):
        self.assertRaises(Exception, self.ec.validate_number, '')

    def test_only_plus(self):
        self.assertRaises(Exception, self.ec.validate_number, '+')

    def test_too_long_number(self):
        self.assertRaises(Exception, self.ec.validate_number,
            '+46123456789123456789')

    def test_alphanum_invalid(self):
        self.assertRaises(Exception, self.ec.validate_number, 'elkme')

class TestFormatSmsPayload(unittest.TestCase):
    ec = elks.Elks()

    def test_message(self):
        message = 'Test Case #1'
        sms = self.ec.format_sms_payload(message, NULROUTE)
        self.assertEqual(sms['message'], message)

    def test_list_message(self):
        message = ['Test', 'Case', '#2']
        sms = self.ec.format_sms_payload(message, NULROUTE)
        self.assertEqual(sms['message'], 'Test Case #2')

    def test_rstrip_message(self):
        message = 'Test Case #3 \n'
        sms = self.ec.format_sms_payload(message, NULROUTE)
        self.assertEqual(sms['message'], 'Test Case #3')

    def test_default_sender(self):
        sms = self.ec.format_sms_payload('msg', NULROUTE)
        self.assertEqual(sms['from'], 'elkme')

    def test_recipient_validation(self):
        self.assertRaises(Exception, self.ec.format_sms_payload, 'msg', 'elkme')

    def test_alphanum_sender(self):
        sms = self.ec.format_sms_payload('msg', NULROUTE, 'AlphaNumb3r')
        self.assertEqual(sms['from'], 'AlphaNumb3r')
