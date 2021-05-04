from service import find_all, delete_special_symbols
from req import get_ar_au

## ['description','tel', 'address', 'ftl', 'sc', 'ads', 'cart', 'sign', 'login', 'ar2k', 'ln20k'] + word cloud
## 
SIZE_MAX = 3200000


def get_page_size(string):
    return len(string)


def get_norm_size(string):
    return round(get_page_size(string)/SIZE_MAX, 3)


def is_description(string):
    try:
        descriptionposition = string.find('description')
        if descriptionposition > 0:
            return 1
        return 0
    except AttributeError:
        return 0


def is_ftl(string):
    try:
        if string.find('featured</h4>') != -1 and string.find('trending</h4>') != -1 and string.find('latest</h4>') != -1 or string.find('no more posts') != -1:
            return 1
        return 0
    except AttributeError:
        return 0


def is_cart(string):
    try:
        if string.find('cart<') != -1 or string.find('basket<') != -1:
            return 1
        return 0
    except AttributeError:
        return 0


def is_signin(string):
    try:
        if string.find('sign in') != -1:
            return 1
        return 0
    except AttributeError:
        return 0


def is_login(string):
    try:
        if string.find('log in') != -1 or string.find('login') != -1:
            return 1
        return 0
    except AttributeError:
        return 0


def get_title(string):
    try:
        start = string.find('<title>')
        end = string.find('</title>')
    except AttributeError:
        return ''
    if (start == -1) or (end == -1):
        return ''
    return delete_special_symbols(string[start + 7:end])


def get_title_h(string, num): #find titles h1, h2, h3
    try:
        start = string.find('<h' + str(num))
        end = -1
        if start != -1:
            temp = string[start + 3: start + 500]
            brack = temp.find('>')
            end = temp.find('</h' + str(num) + '>')
        if (start == -1) or (end == -1):
            return ''
    except AttributeError:
        return ''
    return delete_special_symbols(temp[brack + 1:end])


def clear_brackets(string):
    if type(string) is not str:
        return ''
    is_bracket_exists = True
    while is_bracket_exists:
        start = string.find('<')
        end = string.find('>')
        if end > start and start != -1:
            string = string[:start] + string[end + 1:]
            continue
        if start == -1 or end == -1:
            is_bracket_exists = False
        if end < start:
            return string
    if not is_bracket_exists:
        return string


def sum_headers(string):
    result = ''
    h1 = get_title_h(string, 1)
    h2 = get_title_h(string, 2)
    h3 = get_title_h(string, 3)
    if not h1.isdigit():
        result += h1
    if not h2.isdigit():
        result += h2
    if not h3.isdigit():
        result += h3
    return result


def form_cloud_of_words(string):
    string = str(string)
    if type(string) is not str:
        return 1
    cloud = get_title(string)
    header = sum_headers(string)
    cloud += header
    return clear_brackets(cloud.lower())


def is_tel(string): #add existence of tel
    if string.find("tel:") != -1:
        return 1
    return 0


def is_address(string): #add existence of address
    if string.find("address") != -1:
        return 1
    return 0


def is_inputbox(string): #add existence of Input type
    if string.find("input type:") != -1:
        return 1
    return 0


def is_ads(string): #add existence of ad blocks by keyword "adsby"
    if string.find("adsby") != -1:
        return 1
    return 0


def get_sc(string): #added count of word "search" / lenght of document
    mlist = list(find_all('search', string))
    return round(len(mlist) * 60 / len(string), 3)


def form_query_to_model(url, string): # form ['description','tel', 'address', 
                                 #       'ftl', 'sc', 'ads', 'cart', 
                                 #       'sign', 'login', 'ar2k', 'ln20k'] + word cloud
    if not string:
        return 203
    alexa_aboutus_ranks = get_ar_au(string)
    return [is_description(string), is_tel(string), is_address(string), 
            is_ftl(string), get_sc(string), is_ads(string), is_cart(string),
            is_signin(string), is_login(string), alexa_aboutus_ranks[0], alexa_aboutus_ranks[1],
            form_cloud_of_words(string), -1
            ]