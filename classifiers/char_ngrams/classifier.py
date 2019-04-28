import numpy as np
import datetime
import globals

from ast import literal_eval
from . import vector_handler

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def char_ngrams_classifier(generate_vectors, database_dir = None, clf_iterations = None):
    """
    main function for classifier, manages the process
    :param generate_vectors: boolean value, True to generate vectors, False to use ready vectors
    :param database_dir: directory of the database to generate vectors from
    :return: nothing, prints the result to the command line
    """
    print("[", datetime.datetime.now()-globals.start_time, "] initiating char_ngram classifier")
    if generate_vectors:
        if database_dir != None:
            users_vector, \
            binary_countries_vector \
                = vector_handler.vector_generator(database_dir)
        else:
            raise NameError('Database directory not specified')
    else:  # use the ready vectors from the vectors directory
        try:
            users_vector, \
            binary_countries_vector = \
                vector_handler.vector_loader()
        except NameError:
            print('Cannot load vectors from classifier')
            return

    # MOTIVATION: Once initiated, start lr_classifier immediately
    print ("In-Domain binary classification score: ",
           logistic_regression_classifier(users_vector, binary_countries_vector, iterations_limit=clf_iterations))
# MOTIVATION: Family Classification

# MOTIVATION: Language Classification

def logistic_regression_classifier(users_vector, countries_vector, iterations_limit = 10000):
    """
    :param users_vector: vector of vectors for each user, containing the 1000 most frequent trichars
    :param binary_countries_vector: vector of integers, containing a matching binary/family/language for each user
    :param iterations_limit: limits the iteration of each cross validation score, make it high enough to avoid warnings
    :return: Logistic Regression classification score in 10-fold (value between 0 and 1)
    """
    if iterations_limit is None:
        iterations_limit = 2000
    clf = LogisticRegression(solver='lbfgs', max_iter=iterations_limit)
    print(datetime.datetime.now()-globals.start_time, ": starting cross validation process")
    print (len(users_vector))
    print(len(countries_vector))
    print(iterations_limit)
    classifier_scores = cross_val_score(clf, users_vector, countries_vector, cv=10)
    return np.average(classifier_scores)