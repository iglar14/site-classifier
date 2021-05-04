from urllib.parse import quote
import requests
from service import get_string_after_key, delete_special_symbols


MAX_ALEXA_RANK = 20000


def strip_url_beginning(url: str):
    for prefix in ['http://', 'https://', 'www.']:
        url = url.removeprefix(prefix)
    return url


def specify_scheme(url, scheme='http://'):
    if url.find('://') == -1:
        return scheme + url
    return url


def get_domain_start(url: str) -> int:
    scheme_pos = url.find('://')
    return 0 if scheme_pos == -1 else scheme_pos + 3


def get_main_page_url(url: str):
    domain_end = url.find('/', get_domain_start(url))
    return url if domain_end == -1 else url[:domain_end]


def parse(url): #get content of page
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    try:
        req = requests.get(url, headers={'User-Agent': user_agent}, timeout=10)
    except Exception:
        return 202
    if req.status_code == 200:
        if len(req.text) < 10:
            return 201
        return req.text
    return 201


def get_alexa_rank(string):
    key = 'has Alexa Rank'
    if string.find(key):
        is_found = False
        is_ended = False
        content_part = get_string_after_key(string, key)
        i = 0
        rank = ''
        while not is_ended or i == len(content_part):
            if content_part[i].isdigit():
                is_found = True
                rank += content_part[i]
            else:
                if is_found:
                    is_ended = True
                    return int(rank)
            i += 1
    return MAX_ALEXA_RANK


def parse_and_get_ar(url):
    content = str(parse('https://www.shift4shop.com/lp/alexa-rank/?url=' + quote(url) + '&button='))
    if len(content) == 3:
        return MAX_ALEXA_RANK
    return get_alexa_rank(delete_special_symbols(content))


def is_ar_significant(alexa_rank):
    if alexa_rank < 2000:
        return 1
    return 0


def get_len_parsed_aboutus(url):
    return len(str(parse('https://aboutus.com/' + quote(url))))


def is_au_len_significant(length):
    if length > 20000:
        return 1
    return 0


def get_ar_au(url):
    rlist = []
    rlist.append(is_ar_significant(parse_and_get_ar(url)))
    rlist.append(is_au_len_significant(get_len_parsed_aboutus(url)))
    return rlist