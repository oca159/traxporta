import string
import random


class URLShortener:
    def __init__(self, shortcode_length=6):
        self.url_mapping = {}
        self.base_url = "http://s.com/"
        self.shortcode_length = shortcode_length

    def generate_shortcode(self):
        characters = string.ascii_letters + string.digits
        shortcode = ''.join(random.choice(characters) for _ in range(self.shortcode_length))
        return shortcode

    def shorten_url(self, original_url):
        if original_url in self.url_mapping.values():
            for code, url in self.url_mapping.items():
                if url == original_url:
                    return self.base_url + code

        shortcode = self.generate_shortcode()
        while shortcode in self.url_mapping:
            shortcode = self.generate_shortcode()

        self.url_mapping[shortcode] = original_url
        return self.base_url + shortcode

    def get_original_url(self, shortcode):
        shortcode = shortcode.replace(self.base_url, '')
        return self.url_mapping.get(shortcode, 'URL no encontrada')