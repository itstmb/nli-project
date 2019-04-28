# Char trigrams generation file

import os
import sys
import numpy as np
import heapq  # We use heap queue as a dictionary sorting structure.
import datetime
import globals

from ast import literal_eval
from heapq import heappop

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

sys.path.append("...")  # dynamic path adjustment
from modules import language as lang


def vector_loader():
    globals.start_time = globals.start_time
    print(datetime.datetime.now()-globals.start_time, ": loading users vector from file")
    try:
        users = [literal_eval(line) for line in open("classifiers/char_ngrams/vectors/users.txt", 'r')]
    except IOError:
        print ("Error: File does not appear to exist.")
        return 0

    print(datetime.datetime.now()-globals.start_time, ": loading binary countries vector from file")
    with open('classifiers/char_ngrams/vectors/countries.txt') as f:
        binary_countries_vector = list(f)

    print(datetime.datetime.now()-globals.start_time, ": users, countries vectors initialized")
    return users, binary_countries_vector


def vector_generator(database_dir):
    main_dir = database_dir  # database directory
    globals.start_time = globals.start_time
    print("[",datetime.datetime.now()-globals.start_time,"] initiating char_ngram vector generator")

    for sub_dir in os.scandir(main_dir):
        if sub_dir.name == "europe_data":  # europe_data directory
            in_domain_dict = {}  # saves tri-chars and their count in the entire database

            """ 
            Parse all files and set in_domain_dict to contain all trigram chars
            We expect to have all trigrams in a {trigram_chars, count} format
            """
            for country_dir in os.scandir(sub_dir):  # parse country directories (exm: reddit.Albania.txt.tok.clean)
                print ("[",datetime.datetime.now()-globals.start_time,"] generating",
                       str.split(os.path.basename(country_dir), '.')[1])
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

            print("[",datetime.datetime.now()-globals.start_time,"] in_domain_dict size: ", len(in_domain_dict))
            print("[",datetime.datetime.now()-globals.start_time,"] in_domain_dict initialized, starting fetch using heapq")

            top_trichars = heapq.nlargest(1000, in_domain_dict, key=in_domain_dict.get)  # fetch top 1000 trichars
            in_domain_dict = None  # Free memory

            # Writing the top trichars to file to prevent re-running the iteration
            with open('top_trichars.txt', 'w') as f:
                for trichar in top_trichars:
                    f.write("%s\n" % trichar)
            f.close()
            # READY: top_trichars.txt contains top 1000 trichars

            print("[",datetime.datetime.now()-globals.start_time,
                  "] fetched 1000 top trichars, starting user vectors init")

            # DEBUG: for top_trigram in top_trichars:  # DEBUG: Doesn't print non-english letters. does it even tell?
            # DEBUG:    print(top_trigram)

            trichars_mapper = {}  # saves mapping between trichars and vector index

            for index in range(1000):
                trichars_mapper[heappop(top_trichars)] = index
            # READY: trichars_mapper{} maps the 1000 most common tri-chars in the database to index numbers
            # TEST: Fetched trigrams

            users = []  # this is a vector containing vector entries [[...],[...],...] - each component is a 1000word vec
            countries_of_users = []  # saves the country of each of the users in a vector

            # MOTIVATION: Building a feature vector of the 1000 most common tri-chars for each user
            # MOTIVATION: Building an additional vector in the size of users, representing 0 - native, 1 - non native
            for country_dir in os.scandir(sub_dir):  # parse country directories (exm: reddit.Albania.txt.tok.clean)
                country_name = str.split(os.path.basename(country_dir), '.')[1]  # fetch country from dir (exm: Albania)
                print ("[",datetime.datetime.now()-globals.start_time,"] generating",country_name)
                for user_dir in os.scandir(country_dir):  # parse user directories (exm: user_name)
                    # DEBUG: print("USER: ", user_dir)
                    countries_of_users.append(country_name) # for each user add country_name to the vec for classification
                    user_vector = [0] * 1000
                    for file_dir in os.scandir(user_dir):  # parse chunk files (exm: char_ngram_chunk1)
                        file = open(file_dir, "r", encoding="utf-8")
                        lines = file.readlines()
                        for line in lines:  # parse lines within chunk text
                            if len(line) >= 11:
                                cur_char = 0
                                while cur_char < len(line):
                                    # DEBUG: print (country_dir,":",user_dir,":",file_dir)
                                    trigram = line[cur_char + 1] + line[cur_char + 4] + line[cur_char + 7]
                                    if trigram in trichars_mapper.keys():
                                        user_vector[trichars_mapper.get(trigram)] += 1  # increment user trigram count
                                    cur_char += 11
                    # DEBUG: print(user_vector)
                    users.append(user_vector)  # insert user vector to the vector of users vectors
            # TEST: Initialized vectors correctness
            # READY: users[] contains a 1000 most common tri-chars vector for each user
            # READY: countries_of_users[] contains the country name for each user (index-fit with users[])

            print("[",datetime.datetime.now()-globals.start_time,"] user vectors initialized, starting binary classification")

            # MOTIVATION: Binary Classification
                # MOTIVATION: Convert countries_of_users to Binary (0- non-native speaker, 1- native speaker)
            binary_countries_vector = []
            # MOTIVATION: Use LanguageDict to determine the value for each language
            for country in countries_of_users:
                if lang.LanguageDict.get(country).native:
                    binary_countries_vector.append(1)
                else:
                    binary_countries_vector.append(0)

            # DEBUG: print(binary_countries_vector)
            # DEBUG: print("Users: ",len(users))
            # DEBUG: print("Countries:" ,len(binary_countries_vector))

            # DEBUG: print to files
            with open('classifiers/char_ngrams/vectors/users.txt', 'w') as f:
                for user in users:
                    f.write("%s\n" % user)
            f.close()

            with open('classifiers/char_ngrams/vectors/countries.txt', 'w') as f:
                for country in binary_countries_vector:
                    f.write("%s\n" % country)
            f.close()

            return users, binary_countries_vector

        elif os.path.dirname(sub_dir) == "non_europe_data":
            pass
            # MOTIVATION: similar to in-domain?
