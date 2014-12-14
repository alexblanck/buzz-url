BuzzURL
======
### Learn this one weird trick for making your URL longer

This site is currently hosted on Google App Engine at [http://buzz-url.appspot.com]()

###How it works:

A conventional URL shortener requires a key-value store to hold a mapping from shortened URLs back to the original URL. However, this site is not a URL shortener, it is a URL *elongator*. It does not require a key-value store; the original URLs are stored directly in the lengthened URLs. The lengthened URLs are encoded as a series of technology buzz words.

Without access to the secret keys, it should be impossible to construct a lengthened URL that this site will decode without using the site iteself.

###How to use:

To use this code, you need to create two 256-bit keys. Place these files in a new file called `secrets.py` as two attributes: `AES_KEY` and `HMAC_KEY`. These keys will be picked up by `mapping.py`. Here is an example of a `secrets.py` file (with some obviously insecure keys):

```
AES_KEY = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
HMAC_KEY = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

Then, the site should be ready to deploy to App Engine or to run on the App Engine development server. You can run the unit tests by visiting [*hostname*/_ah/unittest/]()
