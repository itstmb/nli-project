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

    top_trichars = util.load_countries(trichar_file_path)
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

    top_tripos = util.load_countries(tripos_file_path)
    return top_tripos

def generate_top_tripos(save_path):
    log('Generating top trichars')
    all_tripos = {}

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and i.domain == 'in':

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
                                if i == len(pos_tokens) - 3:
                                    pos_tokens[i + 2] = pos_tokens[i + 1][:len(pos_tokens[i + 2]) - 2]
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

    top_unigrams = util.load_countries(unigram_file_path)
    return top_unigrams


def generate_top_unigrams(save_path):
    log('Generating top unigrams')
    all_unigrams = {}
    discard_tokens = {}#{"?", "!", ",", "...", ".", "(", ")", "[", "]", "/", "|",
                 #     "-",":","%",";","'","**","),","^","`", "=","+", "\'\'","``",
                  #    "\"","!,","~","$","&","*","#","--","1","2","3","4","5","6",
                   #   "7","8","9","10","_","20","30","40","50","100"}
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
                                if token not in discard_tokens:
                                    if token not in all_unigrams.keys():
                                        all_unigrams[token] = 1
                                    else:
                                        all_unigrams[token] += 1

    top_unigrams = heapq.nlargest(1000, all_unigrams, key=all_unigrams.get)  # fetch top 1000 unigrams
    util.save_file(save_path, top_unigrams)


def function_words_process(user_dir):
    user_vector = [0] * 1000

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
    function_words = provide_function_words()

    global function_words_map
    function_words_map={}

    for index in range(426):
        function_words_map[heappop(function_words)] = index


def provide_function_words():
    function_words_file_path = Path("vectors_handling/vectors/functionwords/fucnction_words.txt")

    if not util.exists(function_words_file_path): # can't find the file in memory
        log('Cannot find top unigrams file') # redundant
        generate_function_words(function_words_file_path)

    function_words = util.load_countries(function_words_file_path)
    return function_words


def generate_function_words(save_path):
    log('Generating top unigrams')
    FUNCTION_WORDS = {"'d", "'ll", "'m", "'re", "'s", "'ve", "n't", 'a', 'about', 'above', 'according', 'accordingly',
                      'actual', 'actually', 'after', 'afterward', 'afterwards', 'again', 'against', 'ago', 'ah', 'all',
                      'almost', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'an', 'and', 'another',
                      'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'around', 'art', 'as', 'aside', 'at',
                      'away', 'ay', 'back', 'be', 'bear', 'because', 'been', 'before', 'being', 'below', 'beneath',
                      'beside', 'besides', 'better', 'between', 'beyond', 'bid', 'billion', 'billionth', 'both', 'bring',
                      'but', 'by', 'came', 'can', 'cannot', 'canst', 'certain', 'certainly', 'come', 'comes', 'consequently',
                      'could', 'couldnt', 'dear', 'definite', 'definitely', 'despite', 'did', 'do', 'does', 'doing', 'done',
                      'dost', 'doth', 'doubtful', 'doubtfully', 'down', 'due', 'during', 'e.g.', 'each', 'earlier', 'early',
                      'eight', 'eighteen', 'eighteenth', 'eighth', 'eighthly', 'eightieth', 'eighty', 'either', 'eleven',
                      'eleventh', 'else', 'enough', 'enter', 'ere', 'erst', 'even', 'eventually', 'ever', 'every', 'everybody',
                      'everyone', 'everything', 'everywhere', 'example', 'except', 'exeunt', 'exit', 'fact', 'fair', 'far',
                      'farewell', 'few', 'fewer', 'fifteen', 'fifteenth', 'fifth', 'fifthly', 'fiftieth', 'fifty', 'finally',
                      'first', 'firstly', 'five', 'for', 'forever', 'forgo', 'forth', 'fortieth', 'forty', 'four', 'fourteen',
                      'fourteenth', 'fourth', 'fourthly', 'from', 'furthermore', 'generally', 'get', 'gets', 'getting', 'give',
                      'go', 'good', 'got', 'had', 'has', 'hast', 'hath', 'have', 'having', 'he', 'hence', 'her', 'here', 'hers',
                      'herself', 'him', 'himself', 'his', 'hither', 'ho', 'how', 'however', 'hundred', 'hundredth', 'i', 'if',
                      'in', 'indeed', 'instance', 'instead', 'into', 'is', 'it', 'its', 'itself', 'last', 'lastly', 'later',
                      'less', 'let', 'like', 'likely', 'many', 'matter', 'may', 'maybe', 'me', 'might', 'million', 'millionth',
                      'mine', 'more', 'moreover', 'most', 'much', 'must', 'my', 'myself', 'nay', 'near', 'nearby', 'nearly',
                      'neither', 'never', 'nevertheless', 'next', 'nine', 'nineteen', 'nineteenth', 'ninetieth', 'ninety',
                      'ninth', 'ninthly', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere',
                      'o', 'occasionally', 'of', 'off', 'oft', 'often', 'oh', 'on', 'once', 'one', 'only', 'or', 'order',
                      'other', 'others', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'perhaps', 'possible', 'possibly',
                      'presumable', 'presumably', 'previous', 'previously', 'prior', 'probably', 'quite', 'rare', 'rarely',
                      'rather', 'result', 'resulting', 'round', 'said', 'same', 'say', 'second', 'secondly', 'seldom', 'seven',
                      'seventeen', 'seventeenth', 'seventh', 'seventhly', 'seventieth', 'seventy', 'shall', 'shalt', 'she',
                      'should', 'shouldst', 'similarly', 'since', 'six', 'sixteen', 'sixteenth', 'sixth', 'sixthly', 'sixtieth',
                      'sixty', 'so', 'soever', 'some', 'somebody', 'someone', 'something', 'sometimes', 'somewhere',
                      'soon', 'still', 'subsequently', 'such', 'sure', 'tell', 'ten', 'tenth', 'tenthly', 'than', 'that', 'the',
                      'thee', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'therefore', 'these', 'they',
                      'thine', 'third', 'thirdly', 'thirteen', 'thirteenth', 'thirtieth', 'thirty', 'this', 'thither', 'those',
                      'thou', 'though', 'thousand', 'thousandth', 'three', 'thrice', 'through', 'thus', 'thy', 'till', 'tis',
                      'to', 'today', 'tomorrow', 'too', 'towards', 'twas', 'twelfth', 'twelve', 'twentieth', 'twenty', 'twice',
                      'twill', 'two', 'under', 'undergo', 'underneath', 'undoubtedly', 'unless',  'unlikely', 'until', 'unto',
                      'unusual', 'unusually', 'up', 'upon', 'us', 'very', 'was', 'wast', 'way', 'we', 'welcome',
                      'well', 'were', 'what', 'whatever', 'when', 'whence', 'where', 'whereas', 'wherefore', 'whether',
                      'which', 'while', 'whiles', 'whither', 'who', 'whoever', 'whom', 'whose', 'why', 'wil', 'will', 'wilst', 'wilt',
                      'with', 'within', 'without', 'would', 'wouldst', 'ye', 'yes', 'yesterday', 'yet', 'you', 'your', 'yours',
                      'yourself', 'yourselves'}
    util.save_file(save_path, FUNCTION_WORDS)
