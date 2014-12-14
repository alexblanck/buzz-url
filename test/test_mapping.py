# vim: set fileencoding=utf-8 :

import unittest
import mapping

class TestMapping(unittest.TestCase):

    def test_ascii(self):
        url = "http://www.google.com"
        self._assert_success(url)

    def test_utf_8(self):
        url = u"http://www.goögle.com".encode('utf-8')
        self._assert_success(url)

    def test_unicode_fail(self):
        url = u"http://www.goögle.com"
        with self.assertRaises(UnicodeEncodeError):
            mapping.encrypt(url)

    def test_decode_too_short(self):
        encrypted = "solution-connected-flash-convergence-saas-newsjacking-monetize-neuromorphics"
        self._assert_decryption_exception(encrypted)

    def test_decode_incorrect_padding(self):
        encrypted = "solution-connected-flash-convergence-saas-newsjacking-monetize-neuromorphics-connected"
        self._assert_decryption_exception(encrypted)

    def test_decode_invalid_word(self):
        encrypted = "meeep-connected-flash-convergence"
        self._assert_decryption_exception(encrypted)

    def test_decode_hmac_fail(self):
        encrypted = "solution-connected-flash-convergence-saas-newsjacking-monetize-neuromorphics-connected-trending-phablet-pivot-localisation-omnichannel-paas-social-wearable-neuromorphics-responsive-visionary-kernel-platform-migration-vertical-newsjacking-wearable-iot-paas-virtual-hyperconvergence-engagement-leverage-nano-emergent-innovative-interactive-ajax-blockchain-prosumer-millennials-hyperconvergence-cloud-creative-cloud-innovative-immersive-localisation-newsjacking-responsive-interactive-millennials-selfie-innovative-hyperconvergence-nano-leverage-minimalist-mobile-vertical-mobile"
        self._assert_decryption_exception(encrypted)

    def test_decode_gibberish(self):
        encrypted = "dfsaieuw09381904jlkdszm,.zx"
        self._assert_decryption_exception(encrypted)

    def test_decode_empty(self):
        encrypted = ""
        self._assert_decryption_exception(encrypted)

    def _assert_success(self, data):
        """Check that the url encrypts to something that decrypts correctly

        Additionally, do some sanity checks on the encrypted message

        """
        encrypted = mapping.encrypt(data)
        words = encrypted.split("-")

        self.assertEqual(len(words), len(data) + 62)

        for word in words:
            self.assertIn(word, mapping._WORDS)

        decrypted = mapping.decrypt(encrypted)
        
        self.assertEqual(decrypted, data)

    def _assert_decryption_exception(self, data):
        with self.assertRaises(mapping.DecryptionException):
            mapping.decrypt(data)
