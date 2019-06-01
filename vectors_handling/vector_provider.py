from logger import log
from pathlib import Path

import interpreter as i
import util
import vectors_handling.uvg as uvg
import vectors_handling.cvg as cvg


def provide_vectors():
    user_vector = provide_user_vector()
    country_vector = provide_country_vector()
    return user_vector, country_vector


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

