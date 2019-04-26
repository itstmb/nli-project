# Char trigrams generation file

import os
import sys
import heapq  # We use heap queue as a dictionary sorting structure.
from heapq import heappop

# Resources

# Language

class Language(object):
    def __init__(self, native, family, language_name):
        self.native = native
        self.family = family
        self.language_name = language_name

# Trigram Count
class TriCount(object):
    def __init__(self, tri, count):
        self.tri = tri
        self.count = count


"""
Language families:     Germanic, BaltoSlavic, Romance, NativeEnglish ,Albanian, Armenian, NonEuropean,
                       Finno-Permic, AfroAsiatic, Turkic, Hellenic, Finnic, Karto-Zan
"""

Language_dict = {
            'Albania': Language(False, 'Albanian', 'Albania'),
            'Armenia': Language(False, 'Armenian', 'Armenia'),
            'Australia': Language(True, 'NativeEnglish', 'English'),
            'Austria': Language(False, 'Germanic', 'German'),
            'Bosnia': Language(False, 'BaltoSlavic', 'Bosnia'),
            'Bulgaria': Language(False, 'BaltoSlavic', 'Bulgaria'),
            'Canada': Language(True, 'NativeEnglish', 'English'),
            'China': Language(False, 'NonEuropean', 'China'),
            'Croatia': Language(False, 'BaltoSlavic', 'Croatia'),
            'Cyprus': Language(False, 'Hellenic', 'Greece'),
            'Czech': Language(False, 'BaltoSlavic', 'Czech'),
            'Denmark': Language(False, 'Germanic', 'Denmark'),
            'Estonia': Language(False, 'Finnic', 'Estonia'),
            'Finland': Language(False, 'Finnic', 'Finland'),
            'Frace': Language(False, 'Romance', 'France'),
            'Georgia': Language(False, 'Karto-Zan', 'Georgia'),
            'Germany': Language(False, 'Germanic', 'German'),
            'Greece': Language(False, 'Hellenic', 'Greece'),
            'Hungary': Language(False, 'Finno-Permic', 'Hungary'),
            'Iceland': Language(False, 'Germanic', 'Iceland'),
            'Ireland': Language(True, 'NativeEnglish', 'English' ),
            'Israel': Language(False, 'AfroAsiatic', 'Israel'),
            'Italy': Language(False, 'Romance','Italy'),
            'Latvia': Language(False, 'BaltoSlavic', 'Latvia'),
            'Lithuania': Language(False, 'BaltoSlavic', 'Lithuania'),
            'Macedonia': Language(False, 'BaltoSlavic', 'Macedonia'),
            'Malta': Language(False, 'AfroAsiatic', 'Malta'),
            'Mexico': Language(False, 'Romance', 'Spanish'),
            'Moldova': Language(False, 'Romance', 'Romania'),
            'Montenegro': Language(False, 'BaltoSlavic', 'Montenegro'),
            'Netherlands': Language(False, 'Germanic', 'Netherlands'),
            'NewZealand': Language(True, 'NativeEnglish', 'English'),
            'Norway': Language(False, 'Germanic', 'Norway'),
            'Poland': Language(False, 'BaltoSlavic', 'Poland'),
            'Portugal': Language(False, 'Romance', 'Portugal'),
            'Romania': Language(False, 'Romance', 'Romania'),
            'Russia': Language(False, 'BaltoSlavic', 'Russia'),
            'Serbia': Language(False, 'BaltoSlavic', 'Serbia'),
            'Slovakia': Language(False, 'BaltoSlavic', 'Slovakia'),
            'Slovenia': Language(False, 'BaltoSlavic', 'Slovenia'),
            'Spain': Language(False, 'Romance', 'Spanish'),
            'Sweden': Language(False, 'Germanic', 'Sweden'),
            'Turkey': Language(False, 'Turkic', 'Turkey'),
            'UK': Language(True, 'NativeEnglish', 'English'),
            'Ukraine': Language(False, 'BaltoSlavic', 'Ukraine'),
            'US': Language(True, 'Turkic', 'English'),
            'Vietnam': Language(False, 'NonEuropean', 'Vietnam')
}

# Generate dictionary from files

main_dir = sys.argv[1]  # Files directory
# DEBUG i = 0

for sub_dir in os.scandir(main_dir):
    print(sub_dir)  # DEBUG: tracks progress
    if sub_dir.name == "europe_data":  # europe_data directory
        in_domain_dict = {}  # saves tri-chars and their count in the entire database

        """ 
        Parse all files and set in_domain_dict to contain all trigram chars
        We expect to have all trigrams in a {trigram_chars, count} format
        """
        for country_dir in os.scandir(sub_dir):  # parse country directories (exm: reddit.Albania.txt.tok.clean)
            for user_dir in os.scandir(country_dir):  # parse user directories (exm: user_name)
                for file_dir in os.scandir(user_dir):  # parse chunk files (exm: char_ngram_chunk1)
                    trigram_count = 0
                    file = open(file_dir, "r", encoding="utf-8")
                    lines = file.readlines()
                    for line in lines:  # parse lines within chunk text
                        if len(line) >= 11:
                            cur_char = 0
                            while cur_char < len(line):
                                # print (country_dir,":",user_dir,":",file_dir)
                                trigram = line[cur_char + 1] + line[cur_char + 4] + line[cur_char + 7]
                                if trigram not in in_domain_dict.keys():
                                    in_domain_dict[trigram] = 1
                                    trigram_count += 1
                                else:
                                    in_domain_dict[trigram] += 1
                                cur_char += 11
                # DEBUG: print("[", i, "]", " processing user ", user_dir)
                # DEBUG: i += 1
            # DEBUG: print("processing country ", country_dir)
        # READY: in_domain_dict{} contains all tri-chars and their counts

        top_trichars = heapq.nlargest(1000, in_domain_dict)  # fetch top 1000 trichars OPTIMIZE: Faster sort?

        trichars_mapper = {}  # saves mapping between trichars and vector index

        for index in range(1000):
            trichars_mapper[heappop(top_trichars)] = index
        # READY: trichars_mapper{} maps the 1000 most common tri-chars in the database to index numbers
        # TEST: Fetched trigrams

        for top_trigram in top_trichars:  # DEBUG: Doesn't print non-english letters. does it even tell?
            print(top_trigram)

        users = {}  # this user dict contains {user : vector} entries

        # MOTIVATION: Building a feature vector of the 1000 most common tri-chars for each user
        for country_dir in os.scandir(sub_dir):  # parse country directories (exm: reddit.Albania.txt.tok.clean)
            for user_dir in os.scandir(country_dir):  # parse user directories (exm: user_name)
                user_vector = [0] * 1000
                for file_dir in os.scandir(user_dir):  # parse chunk files (exm: char_ngram_chunk1)
                    file = open(file_dir, "r", encoding="utf-8")
                    lines = file.readlines()
                    for line in lines:  # parse lines within chunk text
                        if len(line) >= 11:
                            cur_char = 0
                            while cur_char < len(line):
                                # print (country_dir,":",user_dir,":",file_dir)
                                trigram = line[cur_char + 1] + line[cur_char + 4] + line[cur_char + 7]
                                if trigram in trichars_mapper.keys():
                                    user_vector[trichars_mapper.get(trigram)] += 1  # increment user trigram count
                                cur_char += 11
                users[user_dir] = user_vector # insert {user_name:user_vector} to the users dict
        # TEST: Initialized vectors correctness
        # READY: users{} contains all users and their 1000 most common tri-chars vector

        # MOTIVATION: Classification

        # MOTIVATION: Result analysis

    elif os.path.dirname(sub_dir) == "non_europe_data":
        pass
