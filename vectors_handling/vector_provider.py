from collections import Counter

from utilities.logger import log
from pathlib import Path

import utilities.interpreter as i
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
    classes_size = Counter(country_vector)
    ds_size = min(classes_size, key=classes_size.get)

    user_vector, country_vector = util.shuffle_vectors(user_vector, country_vector)

    new_users = []
    new_countries = []
    class_counter = dict.fromkeys(Counter.keys(),0)  # Initialize all classes counters to 0

    for user,country in zip(user_vector, country_vector):
        if class_counter[country] < ds_size:
            class_counter[country] += 1
            new_users.append(user)
            new_countries.append(country)

    return new_users, new_countries




def provide_user_vector():
    user_file_path = Path("vectors_handling/vectors/" + i.feature + "/users_" + i.domain + ".txt")

    if not util.exists(user_file_path): # can't find the file in memory
        log('Cannot find ' + i.feature + ' ' + i.domain + ' user vectors file') # redundant
        uvg.provide_trichars_map()
        uvg.generate(user_file_path)

    log('Loading user vectors from file')
    user_vector = util.load_users(user_file_path)
    return user_vector


def provide_country_vector():
    country_file_path = Path("vectors_handling/vectors/" + i.feature + "/countries_" + i.domain + ".txt")

    if not util.exists(country_file_path):  # can't find the file in memory
        log('Cannot find ' + i.feature + ' ' + i.domain + ' countries vectors file') # redundant
        cvg.generate(country_file_path)

    log('Loading country vectors from file')
    country_names = util.load_countries(country_file_path)
    country_vector = class_converter(country_names)
    return country_vector


def class_converter(country_names):
    country_vector = []

    if i.type == 'binary':
        for country in country_names:
            if util.LanguageDict.get(country).native:
                country_vector.append(1)
            else:
                country_vector.append(0)

    elif i.type == 'family':
        for country in country_names:
            country_vector.append(util.FamilyToNum[util.LanguageDict.get(country).family])

    elif i.type == 'language':
        for country in country_names:
            country_vector.append(util.LanguageToNum[util.LanguageDict.get(country).name])

    return country_vector

