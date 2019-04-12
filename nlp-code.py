## Char trigrams generation file

import os
import sys


## Resources

# Language
class lang(object):
    def __init__(self, native, family, language_name):
        self.native = native
        self.family = family
        self.language_name = language_name

# Trigram Count
class tri_count(object):
    def __init__(self, tri, count):
        self.tri = tri
        self.count = count

## list of languages creation
#languagues families:   Germanic, BaltoSlavic, Romance, NativeEnglish ,Albanian, Armenian, NonEuropean,
#                       Finno-Permic, AfroAsiatic, Turkic, Hellenic, Finnic, Karto-Zan
languages_dict = {
            'Albania': lang(False, 'Albanian', 'Albania'),
            'Armenia': lang(False, 'Armenian', 'Armenia'),
            'Australia': lang(True, 'NativeEnglish', 'English'),
            'Austria': lang(False, 'Germanic', 'German'),
            'Bosnia': lang(False, 'BaltoSlavic', 'Bosnia'),
            'Bulgaria': lang(False, 'BaltoSlavic', 'Bulgaria'),
            'Canada': lang(True, 'NativeEnglish', 'English'),
            'China': lang(False, 'NonEuropean', 'China'),
            'Croatia': lang(False, 'BaltoSlavic', 'Croatia'),
            'Cyprus': lang(False, 'Hellenic', 'Greece'),
            'Czech': lang(False, 'BaltoSlavic', 'Czech'),
            'Denmark': lang(False, 'Germanic', 'Denmark'),
            'Estonia': lang(False, 'Finnic', 'Estonia'),
            'Finland': lang(False, 'Finnic', 'Finland'),
            'Frace': lang(False, 'Romance', 'France'),
            'Georgia': lang(False, 'Karto-Zan', 'Georgia'),
            'Germany': lang(False, 'Germanic', 'German'),
            'Greece': lang(False, 'Hellenic', 'Greece'),
            'Hungary': lang(False, 'Finno-Permic', 'Hungary'),
            'Iceland': lang(False, 'Germanic', 'Iceland'),
            'Ireland': lang(True, 'NativeEnglish', 'English' ),
            'Israel': lang(False, 'AfroAsiatic', 'Israel'),
            'Italy': lang(False, 'Romance','Italy'),
            'Latvia': lang(False, 'BaltoSlavic', 'Latvia'),
            'Lithuania': lang(False, 'BaltoSlavic', 'Lithuania'),
            'Macedonia': lang(False, 'BaltoSlavic', 'Macedonia'),
            'Malta': lang(False, 'AfroAsiatic', 'Malta'),
            'Mexico': lang(False, 'Romance', 'Spanish'),
            'Moldova': lang(False, 'Romance', 'Romania'),
            'Montenegro': lang(False, 'BaltoSlavic', 'Montenegro'),
            'Netherlands': lang(False, 'Germanic', 'Netherlands'),
            'NewZealand': lang(True, 'NativeEnglish', 'English'),
            'Norway': lang(False, 'Germanic', 'Norway'),
            'Poland': lang(False, 'BaltoSlavic', 'Poland'),
            'Portugal': lang(False, 'Romance', 'Portugal'),
            'Romania': lang(False, 'Romance', 'Romania'),
            'Russia': lang(False, 'BaltoSlavic', 'Russia'),
            'Serbia': lang(False, 'BaltoSlavic', 'Serbia'),
            'Slovakia': lang(False, 'BaltoSlavic', 'Slovakia'),
            'Slovenia': lang(False, 'BaltoSlavic', 'Slovenia'),
            'Spain': lang(False, 'Romance', 'Spanish'),
            'Sweden': lang(False, 'Germanic', 'Sweden'),
            'Turkey': lang(False, 'Turkic', 'Turkey'),
            'UK': lang(True, 'NativeEnglish', 'English'),
            'Ukraine': lang(False, 'BaltoSlavic', 'Ukraine'),
            'US': lang(True, 'Turkic', 'English'),
            'Vietnam': lang(False, 'NonEuropean', 'Vietnam')
}

## Generate dictionary from files

base_path = os.path.dirname(os.path.realpath(__file__));
main_dir = os.path.join(base_path, sys.argv[1])  # Files directory

for sub_dir in main_dir:
    if os.path.dirname(sub_dir) == "europe_data":  # europe_data directory
        in_domain_dict = {}
        for country_dir in sub_dir:
            for user_dir in country_dir:
                for file_dir in user_dir:
                    trigram_count = 0
                    file = open(file_dir, "r")
                    lines = file.readlines()
                    for line in lines:
                        p = 0
                        while p < len(line):
                            trigram = line[p + 1] + line[p + 4] + line[p + 7]
                            if trigram not in in_domain_dict.keys():
                                in_domain_dict[trigram] = 1
                                trigram_count += 1
                            else:
                                in_domain_dict[trigram] += 1
                            p += 11

        tri_count_arr = list()
        for tri, count in in_domain_dict.items():
            tri_count_arr.append(tri_count(tri, count))

        # Sort tri_count_arr

        # Picking top 1000 tri-chars

        # Making user feature vectors

        # classification

    elif os.path.dirname(sub_dir) == "non_europe_data":
        pass