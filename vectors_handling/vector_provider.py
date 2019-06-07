from collections import Counter

from utilities.logger import log
from pathlib import Path

import utilities.interpreter as setup
import utilities.util as util
import vectors_handling.uvg as uvg
import vectors_handling.cvg as cvg


def provide_vectors():
    user_vector = provide_user_vector()
    country_vector = provide_country_vector()
    user_vector, country_vector = downsampler(user_vector, country_vector)
    return user_vector, country_vector


def downsampler(user_vector, country_vector):
    log('Starting downsampling process')
    classes_sizes = Counter(country_vector)
    ds_size = min(classes_sizes.values())

    user_vector, country_vector = util.shuffle_vectors(user_vector, country_vector)

    new_users = []
    new_countries = []
    class_counter = dict.fromkeys(Counter(country_vector), 0)  # Initialize all classes counters to 0
    for user,country in zip(user_vector, country_vector):
        if class_counter[country] < ds_size:
            class_counter[country] += 1
            new_users.append(user)
            new_countries.append(country)

    log('Downsampling results: Class size: ' + str(ds_size) + ', Total data size: ' + str(len(new_countries)))
    return new_users, new_countries


def provide_user_vector():
    user_file_path = Path("vectors_handling/vectors/" + setup.feature + "/users_" + setup.domain + ".txt")

    if not util.exists(user_file_path): # can't find the file in memory
        log('Cannot find ' + setup.feature + ' ' + setup.domain + ' user vectors file') # redundant

        if setup.feature == 'trichar':
            uvg.provide_trichars_map()
        elif setup.feature == 'pos':
            uvg.provide_tripos_map()
        elif setup.feature == 'unigrams':
            uvg.provide_unigrams_map()
        elif setup.feature == 'functionwords':
            uvg.provide_function_words_map()

        uvg.generate(user_file_path)

    log('Loading user vectors from file')
    user_vector = util.load_users(user_file_path)
    return user_vector


def provide_country_vector():
    country_file_path = Path("vectors_handling/vectors/" + setup.feature + "/countries_" + setup.domain + ".txt")

    if not util.exists(country_file_path):  # can't find the file in memory
        log('Cannot find ' + setup.feature + ' ' + setup.domain + ' countries vectors file') # redundant
        cvg.generate(country_file_path)

    log('Loading country vectors from file')
    country_names = util.load_file(country_file_path)
    country_vector = class_converter(country_names)
    return country_vector


def class_converter(country_names):
    country_vector = []

    if setup.type == 'binary':
        for country in country_names:
            if util.LanguageDict.get(country).native:
                country_vector.append(1)
            else:
                country_vector.append(0)

    elif setup.type == 'family':
        for country in country_names:
            country_vector.append(util.FamilyToNum[util.LanguageDict.get(country).family])

    elif setup.type == 'language':
        for country in country_names:
            country_vector.append(util.LanguageToNum[util.LanguageDict.get(country).name])

    return country_vector
