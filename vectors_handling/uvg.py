import os
import re
import heapq

from heapq import heappop

from pathlib import Path
from utilities.logger import log

import utilities.util as util
import utilities.interpreter as setup


def generate(saving_path):
    log('Generating <' + setup.feature + ',' + setup.domain + '> user vectors')

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':
            users = process_dir(domain_dir)
        elif domain_dir.name == 'non_europe_data' and setup.domain == 'out':
            users = process_dir(domain_dir)

    util.save_file(saving_path, users)

def process_dir(domain_dir):
    users = []

    for country_dir in os.scandir(domain_dir):
        country_name = str.split(os.path.basename(country_dir), '.')[1]
        log('Generating users for ' + country_name)
        for user_dir in os.scandir(country_dir):
            users.append(process_user(user_dir))

    return users


def process_user(user_dir):
    if setup.feature == 'trichar':
        return trichar_process(user_dir)
    elif setup.feature == 'pos':
        return pos_process(user_dir)
    elif setup.feature == 'unigrams':
        return token_unigram_process(user_dir)
    elif setup.feature == 'functionwords':
        return function_words_process(user_dir)
    elif setup.feature == 'synchronized_functionwords':
        return syncronized_functionwords_process(user_dir)


def trichar_process(user_dir):
    user_vector = [0] * 1000

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')

        for line in file:
            if len(line) >= 11:
                cur_char = 0
                while cur_char < len(line):
                    trigram = line[cur_char + 1] + line[cur_char + 4] + line[cur_char + 7]
                    if trigram in trichars_map.keys():
                        user_vector[trichars_map.get(trigram)] += 1
                    cur_char += 11

    return user_vector


def provide_trichars_map():
    top_trichars = provide_top_trichars()

    global trichars_map
    trichars_map = {}  # saves mapping between trichars and vector index
    for index in range(1000):
        trichars_map[heappop(top_trichars)] = index

def provide_top_trichars():
    trichar_file_path = Path("vectors_handling/vectors/trichar/top_trichars.txt")

    if not util.exists(trichar_file_path): # can't find the file in memory
        log('Cannot find top trichars file') # redundant
        generate_top_trichars(trichar_file_path)

    top_trichars = util.load_file(trichar_file_path)
    return top_trichars


def generate_top_trichars(save_path):
    log('Generating top trichars')
    all_trichars = {}

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':

            for country_dir in os.scandir(domain_dir):
                country_name = str.split(os.path.basename(country_dir), '.')[1]
                log('Generating top trichars for ' + country_name)
                for user_dir in os.scandir(country_dir):

                    for file_dir in os.scandir(user_dir):
                        file = open(file_dir, "r", encoding="utf-8")
                        lines = file.readlines()
                        for line in lines:  # parse lines within chunk text

                            if len(line) >= 11:
                                cur_char = 0
                                while cur_char < len(line):

                                    trichar = line[cur_char + 1] + line[cur_char + 4] + line[cur_char + 7]
                                    if trichar not in all_trichars.keys():
                                        all_trichars[trichar] = 1
                                    else:
                                        all_trichars[trichar] += 1
                                    cur_char += 11

    top_trichars = heapq.nlargest(1000, all_trichars, key=all_trichars.get)  # fetch top 1000 trichars
    util.save_file(save_path, top_trichars)

def pos_process(user_dir):
    user_vector = [0] * 300

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')

        for line in file:
            pos_tokens = re.split("'\), \('|'\), \(\"", line)
            for i in range(len(pos_tokens)-3):
                trigram = ""
                for j in range(i, i + 2):
                    trigram += re.split("', '|\", '", pos_tokens[j])[1] + " "
                trigram = trigram + re.split("', '|\", '", pos_tokens[i+2])[1]
                if trigram in tripos_map.keys():
                    user_vector[tripos_map.get(trigram)] += 1

    return user_vector

def provide_tripos_map():
    top_tripos = provide_top_tripos()

    global tripos_map
    tripos_map = {}  # saves mapping between tripos and vector index
    for index in range(300):
        tripos_map[heappop(top_tripos)] = index

def provide_top_tripos():
    tripos_file_path = Path("vectors_handling/vectors/pos/top_tripos.txt")

    if not util.exists(tripos_file_path): # can't find the file in memory
        log('Cannot find top tripos file') # redundant
        generate_top_tripos(tripos_file_path)

    top_tripos = util.load_file(tripos_file_path)
    return top_tripos

def generate_top_tripos(save_path):
    log('Generating top trichars')
    all_tripos = {}

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':

            for country_dir in os.scandir(domain_dir):
                country_name = str.split(os.path.basename(country_dir), '.')[1]
                log('Generating top tripos for ' + country_name)
                for user_dir in os.scandir(country_dir):

                    for file_dir in os.scandir(user_dir):
                        file = open(file_dir, "r", encoding="utf-8")
                        lines = file.readlines()

                        for line in lines:  # parse lines within chunk text
                            pos_tokens = re.split("'\), \('|'\), \(\"", line)
                            for i in range(len(pos_tokens) - 3):
                                trigram = ""
                                for j in range(i, i + 2):
                                    trigram = trigram + re.split("', '|\", '", pos_tokens[j])[1] + " "
                                trigram = trigram + re.split("', '|\", '", pos_tokens[i + 2])[1]
                                if trigram not in all_tripos.keys():
                                    all_tripos[trigram] = 1
                                else:
                                    all_tripos[trigram] += 1

    top_tripos = heapq.nlargest(300, all_tripos, key=all_tripos.get)  # fetch top 1000 tripos
    util.save_file(save_path, top_tripos)


def token_unigram_process(user_dir):
    user_vector = [0] * 1000

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        chunk_vector =[0] * 1000
        token_counter = 0
        file_counter=1
        lines = file.readlines()

        for line in lines:
            tokens = line.split()
            for token in tokens:
                token_counter+=1
                if token in unigram_map.keys():
                    chunk_vector[unigram_map.get(token)] += 1

        for index in range(1000):
            chunk_vector[index]/= token_counter
            user_vector[index]+=chunk_vector[index]
        file_counter+=1

    for index in range(1000):
        user_vector[index]/=file_counter

    return user_vector


def provide_unigrams_map():
    top_unigram = provide_top_unigram()

    global unigram_map
    unigram_map ={}

    for index in range(1000):
        unigram_map[heappop(top_unigram)]= index


def provide_top_unigram():
    unigram_file_path = Path("vectors_handling/vectors/unigrams/top_unigrams.txt")

    if not util.exists(unigram_file_path): # can't find the file in memory
        log('Cannot find top unigrams file') # redundant
        generate_top_unigrams(unigram_file_path)

    top_unigrams = util.load_file(unigram_file_path)
    return top_unigrams


def generate_top_unigrams(save_path):
    log('Generating top unigrams')
    all_unigrams = {}

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':

            for country_dir in os.scandir(domain_dir):
                country_name = str.split(os.path.basename(country_dir), '.')[1]
                log('Generating top unigrams for ' + country_name)
                for user_dir in os.scandir(country_dir):

                    for file_dir in os.scandir(user_dir):
                        file = open(file_dir, "r", encoding="utf-8")
                        lines = file.readlines()
                        for line in lines:
                            unigrams = line.split()
                            for token in unigrams:
                                if token not in all_unigrams.keys():
                                    all_unigrams[token] = 1
                                else:
                                    all_unigrams[token] += 1

    top_unigrams = heapq.nlargest(1000, all_unigrams, key=all_unigrams.get)  # fetch top 1000 unigrams
    util.save_file(save_path, top_unigrams)


def function_words_process(user_dir):
    user_vector = [0] * len(function_words_map)

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()

        for line in lines:
            words = line.split()
            for word in words:
                if word in function_words_map.keys():
                    user_vector[function_words_map.get(word)] += 1

    return user_vector


def provide_function_words_map():
    function_words_file_path = Path("vectors_handling/vectors/functionwords/function_words.txt")
    function_words = util.load_file(function_words_file_path)
    global function_words_map
    function_words_map={}

    for index in range(len(function_words)):
        function_words_map[heappop(function_words)] = index


def syncronized_functionwords_process(user_dir):

    provide_courpus_functionwords(setup.numOfFunctionwords)

    user_vector = [0]*len(top_corpus_functionwords)
    indexed_top_corpus_functionwords={}

    index=0
    for word in top_corpus_functionwords:
        indexed_top_corpus_functionwords[word]=index
        index +=1

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()

        for line in lines:
            words = line.split()
            for word in words:
                if word in top_corpus_functionwords:
                    user_vector[indexed_top_corpus_functionwords.get(word)] += 1

    return user_vector

def provide_courpus_functionwords(numOfFunctionwords):

    global top_corpus_functionwords
    top_corpus_functionwords={}

    synchronized_functionwords_file_path = Path("vectors_handling/vectors/synchronized_functionwords/synchronized_functionwords.txt")

    if not util.exists(synchronized_functionwords_file_path):  # can't find the file in memory
        log('Cannot find synchronized_functionwords file')  # redundant

        corpus_functionwords = {}

        for domain_dir in os.scandir(setup.database):
            if domain_dir.name == 'europe_data' and setup.domain == 'in':
                for country_dir in os.scandir(domain_dir):
                    country_name = str.split(os.path.basename(country_dir), '.')[1]
                    log('Counting function words in ' + country_name)
                    for user_dir in os.scandir(country_dir):
                        for file_dir in os.scandir(user_dir):
                            file = open(file_dir, "r", encoding="utf-8")
                            lines = file.readlines()
                            for line in lines:
                                words = line.split()
                                for word in words:
                                    if word in function_words_map.keys():
                                        if word not in corpus_functionwords.keys():
                                            corpus_functionwords[word] = 1
                                        else:
                                            corpus_functionwords[word] += 1

        top_corpus_functionwords = heapq.nlargest(numOfFunctionwords, corpus_functionwords,
                                                  key=corpus_functionwords.get)
        util.save_file(synchronized_functionwords_file_path, top_corpus_functionwords)

    top_corpus_functionwords = util.load_file(synchronized_functionwords_file_path)
    return top_corpus_functionwords
