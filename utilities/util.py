import os
import errno
import datetime
import random

import utilities.interpreter as i

from ast import literal_eval

class Language(object):
    def __init__(self, native, family, name):
        self.native = native
        self.family = family
        self.name = name


LanguageDict = {
    'Albania': Language(False, 'Other', 'Albania'),
    'Armenia': Language(False, 'Other', 'Armenia'),
    'Australia': Language(True, 'NativeEnglish', 'English'),
    'Austria': Language(False, 'Germanic', 'German'),
    'Bosnia': Language(False, 'BaltoSlavic', 'Bosnia'),
    'Bulgaria': Language(False, 'BaltoSlavic', 'Bulgaria'),
    'Canada': Language(True, 'NativeEnglish', 'English'),
    'China': Language(False, 'Other', 'China'),
    'Croatia': Language(False, 'BaltoSlavic', 'Croatia'),
    'Cyprus': Language(False, 'Other', 'Greece'),
    'Czech': Language(False, 'BaltoSlavic', 'Czech'),
    'Denmark': Language(False, 'Germanic', 'Denmark'),
    'Estonia': Language(False, 'BaltoSlavic', 'Estonia'),
    'Finland': Language(False, 'Other' , 'Finland'),
    'France': Language(False, 'Latin', 'France'),
    'Georgia': Language(False, 'Other', 'Georgia'),
    'Germany': Language(False, 'Germanic', 'German'),
    'Greece': Language(False, 'Other', 'Greece'),
    'Hungary': Language(False, 'Other', 'Hungary'),
    'Iceland': Language(False, 'Germanic', 'Iceland'),
    'Ireland': Language(True, 'NativeEnglish', 'English'),
    'India': Language(False, 'Other', 'India'),
    'Israel': Language(False, 'Other', 'Israel'),
    'Italy': Language(False, 'Latin', 'Italy'),
    'Latvia': Language(False, 'BaltoSlavic', 'Latvia'),
    'Lithuania': Language(False, 'BaltoSlavic', 'Lithuania'),
    'Macedonia': Language(False, 'BaltoSlavic', 'Macedonia'),
    'Malta': Language(False, 'Latin', 'Malta'),
    'Mexico': Language(False, 'Latin', 'Spanish'),
    'Moldova': Language(False, 'Latin', 'Romania'),
    'Montenegro': Language(False, 'BaltoSlavic', 'Montenegro'),
    'Netherlands': Language(False, 'Germanic', 'Netherlands'),
    'NewZealand': Language(True, 'NativeEnglish', 'English'),
    'Norway': Language(False, 'Germanic' , 'Norway'),
    'Poland': Language(False, 'BaltoSlavic', 'Poland'),
    'Portugal': Language(False, 'Latin', 'Portugal'),
    'Romania': Language(False, 'Latin', 'Romania'),
    'Russia': Language(False, 'BaltoSlavic', 'Russia'),
    'Serbia': Language(False, 'BaltoSlavic', 'Serbia'),
    'Slovakia': Language(False, 'BaltoSlavic',  'Slovakia'),
    'Slovenia': Language(False, 'BaltoSlavic', 'Slovenia'),
    'Spain': Language(False, 'Latin', 'Spanish'),
    'Sweden': Language(False, 'Germanic', 'Sweden'),
    'Turkey': Language(False, 'Other', 'Turkey'),
    'UK': Language(True, 'NativeEnglish', 'English'),
    'Ukraine': Language(False, 'BaltoSlavic', 'Ukraine'),
    'US': Language(True, 'NativeEnglish', 'English'),
    'Vietnam': Language(False, 'Other', 'Vietnam')
}

# Maps language families to numbers for family classification
FamilyToNum = {
    'Germanic': 0,
    'BaltoSlavic': 1,
    'NativeEnglish': 2,
    'Latin': 3,
    'Other': 4
}

# Maps languages to numbers for language classification
LanguageToNum = {
    'Albania': 0,
    'Armenia': 1,
    'English': 2,
    'German': 3,
    'Bosnia': 4,
    'Bulgaria': 5,
    # 'China': 6,
    'Croatia': 7,
    'Greece': 8,
    'Czech': 9,
    'Denmark': 10,
    'Estonia': 11,
    'Finland': 12,
    'France': 13,
    'Georgia': 14,
    'Hungary': 15,
    'Iceland': 16,
    'India': 17,
    'Israel': 18,
    'Italy': 19,
    'Latvia': 20,
    'Lithuania': 21,
    'Macedonia': 22,
    'Malta': 23,
    'Spanish': 24,
    'Romania': 25,
    # 'Montenegro': 26,
    'Netherlands': 27,
    'Norway': 28,
    'Poland': 29,
    'Portugal': 30,
    'Russia': 31,
    'Serbia': 32,
    'Slovakia': 33,
    'Slovenia': 34,
    'Sweden': 35,
    'Turkey': 36,
    'Ukraine': 37
    # 'Vietnam': 38
}


FeatureToDirectory = {
    'trichar': '/char_ngrams_chunks.tar/char_ngrams_chunks',
    'pos': '/pos_chunks.tar/pos_chunks-004/pos_chunks'
}


def get_time():
    return datetime.datetime.now().strftime("%X")


# Takes 2 vectors and shuffles while keeping them in the same {a,b} fitting.
def shuffle_vectors(vector_a, vector_b):
    combined_vector = list(zip(vector_a,vector_b))
    random.shuffle(combined_vector)
    vector_a, vector_b = zip(*combined_vector)
    return vector_a, vector_b


def exists(path):
    if path.is_file():
        return True
    return False


def save_file(path, data_list):

    # check / create directory
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # write file
    with open(path, 'w') as f:
        for data in data_list:
            f.write('%s\n' % data)
    f.close()


def write_scores(score):
    score_info = '[{}]:\n' \
                 'feature: {}\n' \
                 'type: {}\n' \
                 'domain: {}\n' \
                 'threads: {}\n' \
                 'max iterations: {}' \
                 'score: {}'.format(get_time(),
                                    i.feature,
                                    i.type,
                                    i.domain,
                                    i.threads,
                                    i.iterations,
                                    score)

    write_to_file(score_info)


def write_to_file(data):
    with open('results.txt', 'a') as f:
        f.write('______\n%s\n' % data)


def load_countries(path):
    try:
        with open(path) as f:
            countries_names = f.read().splitlines()
    except IOError:
        raise IOError('Error: Error loading file from path: ', path)
    return countries_names

def load_users(path):
    try:
        in_users = [literal_eval(line) for line in open(path, 'r')]
    except IOError:
        print ("Error: File does not appear to exist.")
        return 0

    return in_users

