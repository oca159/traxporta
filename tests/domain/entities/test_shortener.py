import string

from domain.entities.shortener import URLShortener


def test_generate_shortcode_length():
    shortener = URLShortener()
    shortcode = shortener.generate_shortcode()
    assert len(shortcode) == shortener.shortcode_length
    assert all(c in string.ascii_letters + string.digits for c in shortcode)


def test_shorten_url_new_url():
    shortener = URLShortener()
    original_url = "https://example.com"
    short_url = shortener.shorten_url(original_url)
    assert short_url.startswith(shortener.base_url)
    assert short_url[len(shortener.base_url):] in shortener.url_mapping


def test_shorten_url_same_url():
    shortener = URLShortener()
    original_url = "https://example.com"
    first_short_url = shortener.shorten_url(original_url)
    second_short_url = shortener.shorten_url(original_url)
    assert first_short_url == second_short_url


def test_get_original_url_valid_shortcode():
    shortener = URLShortener()
    original_url = "https://example.com"
    short_url = shortener.shorten_url(original_url)
    retrieved_url = shortener.get_original_url(short_url)
    assert retrieved_url == original_url


def test_get_original_url_invalid_shortcode():
    shortener = URLShortener()
    invalid_shortcode = "http://s.com/abcdef"
    retrieved_url = shortener.get_original_url(invalid_shortcode)
    assert retrieved_url == 'URL no encontrada'