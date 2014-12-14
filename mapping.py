import logging
import binascii
import base64
import itertools
import secrets

from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

# Many parts of this file are adapted from simple-crypt
# https://github.com/andrewcooke/simple-crypt

HALF_BLOCK_BYTES = AES.block_size // 2
HALF_BLOCK_BITS = HALF_BLOCK_BYTES * 8
HASH = SHA256
HEADER = b'\x00'

AES_KEY = secrets.AES_KEY
HMAC_KEY = secrets.HMAC_KEY

assert isinstance(AES_KEY, str)
assert isinstance(HMAC_KEY, str)
assert len(AES_KEY) == 32
assert len(HMAC_KEY) == 32

def encrypt(data):
    # Use a static header for now
    header = HEADER
    
    # Pick a random nonce
    # Use it as the counter prefix
    nonce = get_random_bytes(HALF_BLOCK_BITS//8)

    # Create a counter with the first half as a set prefix
    # and the second half as a counter
    counter = Counter.new(HALF_BLOCK_BITS, prefix=nonce)
    
    cipher = AES.new(AES_KEY, AES.MODE_CTR, counter=counter)
    encrypted = cipher.encrypt(data)

    hmac = _hmac(HMAC_KEY, nonce + header + encrypted)
    payload = nonce + header + encrypted + hmac

    return _encode(payload)

def decrypt(payload):
    data = _decode(payload)
    
    if len(data) < 1 + HALF_BLOCK_BYTES + HASH.digest_size:
        raise DecryptionException("Data is not long enough to decrypt")

    # Extract the header, nonce, encrypted data, and hmac from the data
    nonce = data[:HALF_BLOCK_BYTES]
    header = data[HALF_BLOCK_BYTES:1+HALF_BLOCK_BYTES]
    encrypted = data[1+HALF_BLOCK_BYTES:-HASH.digest_size]
    hmac = data[-HASH.digest_size:]

    # Ensure the HMAC matches what we expect
    expected_hmac = _hmac(HMAC_KEY, nonce + header + encrypted)
    _assert_hmac_match(HMAC_KEY, hmac, expected_hmac)

    # Create a counter with the first half as a set prefix
    # and the second half as a counter
    counter = Counter.new(HALF_BLOCK_BITS, prefix=nonce)
    
    cipher = AES.new(AES_KEY, AES.MODE_CTR, counter=counter)
    return cipher.decrypt(encrypted)

class DecryptionException(Exception): pass

def _encode(s):
    """Encodes a byte string into a string of words

    """
    s = base64.b64encode(s)
    # Strip out any padding
    # This prevents duplicate instances of the same word at the end of the string
    s = s.rstrip("=")
    s = "-".join(_b64_to_word(c) for c in s)
    return s

def _decode(s):
    """Decodes a string of words back to a byte string

    """
    s = ''.join(_word_to_b64(w) for w in s.split('-'))

    # Add padding to make the string length a multiple of 4
    s += "=" * (-len(s) % 4)
    try:
        s = base64.b64decode(s)
    except TypeError, e:
        raise DecryptionException("Padding on base64 string was incorrect")

    return s

def _hmac(key, data):
    """Returns an HMAC byte string that can be used to verify that we were the ones who actually encrypted the message

    """
    return HMAC.new(key, data, HASH).digest()

def _assert_hmac_match(key, actual_hmac, expected_hmac):
    """Asserts that two hmac strings match

    But does this in a way that prevents timing attacks on the string comparison
    """
    # https://www.isecpartners.com/news-events/news/2011/february/double-hmac-verification.aspx
    if _hmac(key, actual_hmac) != _hmac(key, expected_hmac):
        raise DecryptionException("HMAC strings do not match. The data we're trying to decrypt may have been tampered with")

#
# Code for mapping from base64 characters to words 
#

_CHARACTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "/",
    "+"
]

_WORDS = [
    "cloud",
    "phablet",
    "pivot",
    "leverage",
    "responsive",
    "ajax",
    "mobile",
    "viral",
    "disruptive",
    "trending",
    "buzz",
    "synergy",
    "minimalist",
    "flat",
    "material",
    "ubiquitous",
    "parallax",
    "interactive",
    "freemium",
    "gamification",
    "social",
    "engagement",
    "effective",
    "creative",
    "visionary",
    "convergence",
    "solution",
    "prosumer",
    "ninja",
    "app",
    "connected",
    "petaflop",
    "petabyte",
    "saas",
    "paas",
    "iaas",
    "flash",
    "nano",
    "kernel",
    "gigapixel",
    "robust",
    "migration",
    "paradigm",
    "wearable",
    "iot",
    "integrated",
    "hyperconvergence",
    "millennials",
    "localisation",
    "viewability",
    "newsjacking",
    "omnichannel",
    "neuromorphics",
    "immersive",
    "selfie",
    "blockchain",
    "digerati",
    "innovative",
    "virtual",
    "monetize",
    "vertical",
    "emergent",
    "platform",
    "enterprise"
]

# Sanity checks for duplicates
assert len(set(_WORDS)) == len(_WORDS)
assert len(set(_CHARACTERS)) == len(_CHARACTERS)

# Sanity check for BASE64 (without '=' character)
assert len(_WORDS) == 64
assert len(_CHARACTERS) == 64

# Create maps for encoding and decoding
_WORD_TO_CHARACTER = dict(itertools.izip(_WORDS, _CHARACTERS))
_CHARACTER_TO_WORD = dict(itertools.izip(_CHARACTERS, _WORDS))

def _b64_to_word(c):
    return _CHARACTER_TO_WORD[c]

def _word_to_b64(word):
    try:
        return _WORD_TO_CHARACTER[word]
    except KeyError:
        raise DecryptionException("Encountered an unknown word")
