import requests
from service import find_all, get_string_after_key, delete_special_symbols

def get_actual_user_agent(): 
    url = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome'
    req = requests.get(url, timeout = 10)
    if req.status_code != 200:
        return 1
    start = req.text.find('Mozilla')
    end = req.text[start:].find('</span>')
    if start > end:
        return 1
    return req.text[start:start + end]


def prepare_domain_url(url):
    return prepare_url(get_main_page_url(url))


def prepare_url(url):
    dotscount = list(find_all('.', url))
    if len(dotscount) > 2:
        url = url[:4] + url[dotscount[size-2]+1:]
    if url.find('http') == -1:
        return 'http://' + url
    return url

    
def get_main_page_url(url):
    slash = list(find_all('/', url))
    if len(slash) < 3:
        return url
    return url[:slash[2]]


def parse(url): #get content of page
    #user_agent = get_actual_user_agent()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    try:
        req = requests.get(url, headers={'User-Agent':user_agent}, timeout = 10)
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
    return 20000

def parse_and_get_ar(url):
    content = str(parse('https://www.shift4shop.com/lp/alexa-rank/?url=' + url + '&button='))
    if len(content) == 3:
        return 20000
    return get_alexa_rank(delete_special_symbols(content))

def is_ar_below_2000(alexa_rank):
    try:   
        if alexa_rank < 2000:
            return 1
        return 0
    except Exception:
        return 0

def get_len_parsed_aboutus(url):
    return len(str(parse('https://aboutus.com/' + url)))

def is_au_len_over_20000(length):
    try:
        if length > 20000:
            return 1
        return 0
    except Exception:
        return 0

def get_ar_au(url):
    rlist = []
    rlist.append(is_ar_below_2000(parse_and_get_ar(url)))
    rlist.append(is_au_len_over_20000(get_len_parsed_aboutus(url)))
    return rlist