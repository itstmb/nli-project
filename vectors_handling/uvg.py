import os
import re
import heapq
import json

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
    elif setup.feature == 'bipos':
        return bipos_process(user_dir)
    elif setup.feature == 'unigrams':
        return token_unigram_process(user_dir)
    elif setup.feature == 'functionwords':
        return function_words_process(user_dir)
    elif setup.feature == 'synchronized_functionwords':
        return syncronized_functionwords_process(user_dir)
    elif setup.feature == 'avgcapital':
        return avgcapital_process(user_dir)
    elif setup.feature == 'numberwords':
        return numberwords_process(user_dir)
    elif setup.feature == 'punctuations':
        return punctuations_process(user_dir)
    elif setup.feature == 'edit_distance':
        return edit_distance_process(user_dir)
    elif setup.feature == 'spelling_errors':
        return spelling_errors_process(user_dir)
    elif setup.feature == 'country_words':
        return country_words_process(user_dir)
    elif setup.feature == 'avg_word':
        return average_word_process(user_dir)
    elif setup.feature == 'english':
        return average_english(user_dir)

def punctuations_process(user_dir):
    user_vector = [0]*9
    # [cell 0][cell 1][cell 2 ][cell 3 ][cell 4][cell 5][cell 6][cell 7][cell 8]
    # [  ,  ][   .   ][   ?   ][   !   ][   -  ][   :  ][   ;  ][   "  ][   '  ]
    punctuations={',':'0', '.':'1', '?':'2','!':'3', '-':'4',':':'5',';':'6','"':'7',"'":'8'}
    sum=0
    totalfiles = len(os.listdir(user_dir))
    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            words = re.split(" ",line)
            for word in words:
                for char in word:
                    if char in punctuations.keys():
                        user_vector[int(punctuations.get(char))]+=1
                        sum+=1

    for i in range(8):
        user_vector[i]/=totalfiles

    # user_name = os.path.basename(user_dir)
    # log('User vector for ' + user_name+' is:')
    # print(user_vector)
    return user_vector


def numberwords_process(user_dir):
    user_vector=[0]*2
    numcounter=0
    wordscounter=0
    avgnumfile=0
    avgwordfile=0
    finalavgnum=0
    finalavgword=0
    totalfiles = len(os.listdir(user_dir))

    wordnumbers=["one","two","three","four","five","six","seven","eight","nine","ten",
             "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen",
             "eighteen","nineteen","twenty","thirty","forty", "fifty","sixty",
             "seventy","eighty","ninety", "hundred","1k", "2k", "3k", "4k", "5k"]
    numbers =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
              '17','18','19','20','30','40','50','60','70','80','90','100','1000',
              '2000','3000','4000']
    for file_dir in os.scandir(user_dir):
        numcounter=0
        wordscounter=0
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            words = re.split(" ",line)
            for word in words:
                if word in wordnumbers:
                    wordscounter+=1
                elif word in numbers:
                    numcounter+=1
        finalavgnum += numcounter / len(lines)
        finalavgword += wordscounter / len(lines)

    user_vector[0]=finalavgword/totalfiles
    user_vector[1]=finalavgnum/totalfiles
    # user_name = os.path.basename(user_dir)
    # log('User vector for ' + user_name+' is:')
    # print(user_vector)
    return user_vector


def avgcapital_process(user_dir):
    user_vector=[0]
    capitalCounter =0
    totalavg=0
    avgperline=0
    avgperfile=0
    totalfiles = len(os.listdir(user_dir))

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            words = re.split(" ",line)
            for word in words:
                for char in word:
                    if (char.isupper()) == True:
                        print("TEST")
                        capitalCounter += 1
            avgperline = capitalCounter / len(line)
            totalavg += avgperline
            capitalCounter = 0

        avgperfile += totalavg/len(lines)
        totalavg =0
    # user_name = os.path.basename(user_dir)
    user_vector[0]=avgperfile/totalfiles
    # log('User vector for ' + user_name+' is:')
    # print(user_vector[0])
    return user_vector

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

    if not util.exists(tripos_file_path):  # can't find the file in memory
        log('Cannot find top tripos file')  # redundant
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

    provide_corpus_functionwords(setup.numOfFunctionwords)

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


def provide_corpus_functionwords(numOfFunctionwords):
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


def provide_bipos_map():
    top_bipos = provide_top_bipos()

    global bipos_map
    bipos_map = {}  # saves mapping between tripos and vector index
    for index in range(300):
        bipos_map[heappop(top_bipos)] = index


def bipos_process(user_dir):
    user_vector = [0] * 300

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')

        for line in file:
            pos_tokens = re.split("'\), \('|'\), \(\"", line)
            for i in range(len(pos_tokens)-2):
                bigram = ""
                for j in range(i, i + 1):
                    bigram += re.split("', '|\", '", pos_tokens[j])[1] + " "
                    bigram = bigram + re.split("', '|\", '", pos_tokens[i+1])[1]
                if bigram in bipos_map.keys():
                    user_vector[bipos_map.get(bigram)] += 1

    return user_vector


def provide_top_bipos():
    bipos_file_path = Path("vectors_handling/vectors/bipos/top_bipos.txt")

    if not util.exists(bipos_file_path):  # can't find the file in memory
        log('Cannot find top bipos file')  # redundant
        generate_top_bipos(bipos_file_path)

    top_bipos = util.load_file(bipos_file_path)
    return top_bipos


def generate_top_bipos(save_path):
    log('Generating top bichars')
    all_bipos = {}

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':

            for country_dir in os.scandir(domain_dir):
                country_name = str.split(os.path.basename(country_dir), '.')[1]
                log('Generating top bipos for ' + country_name)
                for user_dir in os.scandir(country_dir):

                    for file_dir in os.scandir(user_dir):
                        file = open(file_dir, "r", encoding="utf-8")
                        lines = file.readlines()

                        for line in lines:  # parse lines within chunk text
                            pos_tokens = re.split("'\), \('|'\), \(\"", line)
                            for i in range(len(pos_tokens) - 2):
                                bigram = ""
                                bigram = bigram + re.split("', '|\", '", pos_tokens[i])[1] + " "
                                bigram = bigram + re.split("', '|\", '", pos_tokens[i + 1])[1]
                                if bigram not in all_bipos.keys():
                                    all_bipos[bigram] = 1
                                else:
                                    all_bipos[bigram] += 1

    top_bipos = heapq.nlargest(300, all_bipos, key=all_bipos.get)  # fetch top 300 bipos
    util.save_file(save_path, top_bipos)


def edit_distance_process(user_dir):

    total_edit_distance = 0
    word_count = 0

    for file_dir in os.scandir(user_dir):  # Iterate files
        file = open(file_dir, 'r', encoding='utf-8')

        for line in file:  # Iterate lines
            tokens = re.split("}, {",line)
            for token in tokens:
                word_count += 1
                edit_dist_index = token.find("\"edit_dist\"")
                if edit_dist_index != -1:
                    if token[edit_dist_index+14] in (','):
                        total_edit_distance += int(token[edit_dist_index+13])
                    else:  # Edit distance is a 2 digit number
                        total_edit_distance += int(token[edit_dist_index+13] + token[edit_dist_index+14])

    average_edit_distance = []
    average_edit_distance.append(total_edit_distance / word_count)
    return average_edit_distance

def provide_spelling_map():
    top_spelling = provide_top_spelling_errors()

    global spelling_errors_map
    spelling_errors_map = {}

    for index in range(400):
        spelling_errors_map[heappop(top_spelling)] = index


def provide_top_spelling_errors():
    spelling_file_path = Path("vectors_handling/vectors/spelling_errors/top_spelling_errors.txt")

    if not util.exists(spelling_file_path):  # can't find the file in memory
        log('Cannot find top bipos file')  # redundant
        generate_top_spelling_errors(spelling_file_path)

    top_spelling_errors = util.load_file(spelling_file_path)
    return top_spelling_errors


def generate_top_spelling_errors(save_path):
    log('Generating top spelling errors')
    all_spelling_errors = {}

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':

            for country_dir in os.scandir(domain_dir):
                country_name = str.split(os.path.basename(country_dir), '.')[1]
                log('Generating top spelling errors for ' + country_name)
                for user_dir in os.scandir(country_dir):
                    errors = []
                    for file_dir in os.scandir(user_dir):
                        file = open(file_dir, "r", encoding="utf-8")
                        lines = file.readlines()

                        for line in lines:  # parse lines within chunk text
                            json_data = json.loads(line)
                            for json_token in json_data:
                                if 'deletions' in json_token:
                                    if '[]' not in str(json_token['deletions']):  # not empty
                                        for component in json_token['deletions']:
                                            errors.append("del: " + component)

                                if 'insertions' in json_token:
                                    if '[]' not in str(json_token['insertions']):  # not empty
                                        for component in json_token['insertions']:
                                            errors.append("ins: " + component)

                                if 'replacements' in json_token:
                                    if '[]' not in str(json_token['replacements']):  # not empty
                                        for component in json_token['replacements']:
                                            errors.append("rep: " + str(component))

                    for error in errors:
                        if error not in all_spelling_errors.keys():
                            all_spelling_errors[error] = 1
                        else:
                            all_spelling_errors[error] += 1
    top_spelling_errors = heapq.nlargest(400, all_spelling_errors, key=all_spelling_errors.get)  # fetch top 400 spelling errors
    util.save_file(save_path, top_spelling_errors)


def spelling_errors_process(user_dir):
    user_vector = [0] * 400

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, "r", encoding="utf-8")
        lines = file.readlines()

        for line in lines:  # parse lines within chunk text
            json_data = json.loads(line)
            for json_token in json_data:
                if 'deletions' in json_token:
                    if '[]' not in str(json_token['deletions']):  # not empty
                        for component in json_token['deletions']:
                            token = ("del: " + component)
                            if token in spelling_errors_map:
                                user_vector[spelling_errors_map[token]] += 1


                if 'insertions' in json_token:
                    if '[]' not in str(json_token['insertions']):  # not empty
                        for component in json_token['insertions']:
                            token = ("ins: " + component)
                            if token in spelling_errors_map:
                                user_vector[spelling_errors_map[token]] += 1

                if 'replacements' in json_token:
                    if '[]' not in str(json_token['replacements']):  # not empty
                        for component in json_token['replacements']:
                            token = ("rep: " + str(component))
                            if token in spelling_errors_map:
                                user_vector[spelling_errors_map[token]] += 1

    return user_vector




def country_words_process(user_dir):

    vector = [0]*35

    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()

        for line in lines:
            words = line.split()
            for word in words:
                if word in util.CountryWords:
                    vector[util.CountryWords.get(word)] += 1

    return vector


def average_word_process(user_dir):
    user_chars = 0
    user_words = 0
    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            words = re.split(" ",line)
            user_words += len(words)
            for word in words:
                user_chars += len(word)

    average_word_length = [user_chars/user_words]
    return average_word_length


def average_english(user_dir):
    user_words = 0
    english_words = 0
    for file_dir in os.scandir(user_dir):
        file = open(file_dir, 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            words = re.split(" ",line)
            user_words += len(words)
            for word in words:
                if word == 'english':
                    english_words += 1

    average_english_word = [english_words/user_words]
    return average_english_word