ERRORS = {
    200: 'OK',
    201: 'Cannot load page',
    202: 'Invalid URL',
    203: 'No content from parsing',
    204: 'There are only 5 available urls to classify',
    205: 'There are no parsed url'
    }


import json
import pickle


def save_to_json(dictionary, filename): # serialize data into file:
    json.dump(dictionary, open(filename + ".json", 'w'))

def load_from_json(filename): # read data from file:
    return json.load(open(filename + ".json"))

def save_to_txt(mlist, filename): # save list to txt file
    with open(filename, 'wb') as fp:
        pickle.dump(mlist, fp)

def load_from_txt(filename): # load list from txt file
    with open (filename, 'rb') as fp:
        return pickle.load(fp)


# Find all substrings in string
def find_all(p, s):
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def get_error_encode(num):
    try:
        res = ERRORS[num]
        return res
    except Exception:
        return 'Unknown code'

def get_string_after_key(string, key):
    return string[string.find(key)+len(key):]

def delete_special_symbols(string):
    f = [string]
    f = [x.replace('\n','').replace('&amp;','').replace('|','').replace('-','').replace('?','').replace('\t','').replace('&gt','') for x in f]
    return f[0]