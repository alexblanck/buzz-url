import webapp2
import logging
import mapping
from helpers import write_template
from helpers import write_json

class MainHandler(webapp2.RequestHandler):
    def get(self):
        write_template(self, "main.html", {})

class ElongateHandler(webapp2.RequestHandler):
    def post(self):
        initial = self.request.get("url")

        # Do a super basic and questionable check for valid urls
        if not (initial.startswith("http://") or initial.startswith("https://")):
            self.set_invalid_url_response(initial)
            return;

        # Ensure the user only input ASCII characters
        # Unicode characters in URLs should have been percent-encoded
        try:
            initial = initial.encode('ascii')
        except UnicodeEncodeError:
            self.set_invalid_url_response(initial)
            return;
             

        encrypted = mapping.encrypt(initial)

        buzz_url = self.request.host_url + "/" + encrypted

        write_json(self, {'url': buzz_url})

    def set_invalid_url_response(self, url):
        logging.warning("Invalid URL=%s", url)
        self.response.status = 400

class RedirectHandler(webapp2.RequestHandler):
    def get(self, buzz_url):
        try:
            decrypted = mapping.decrypt(buzz_url)
        except mapping.DecryptionException as e:
            logging.warning("Problem Decrypting: %s", e)
            self.abort(404)
            return

        self.redirect(decrypted)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/elongate', ElongateHandler),
    webapp2.Route('/<buzz_url>', RedirectHandler),
], debug=True)
