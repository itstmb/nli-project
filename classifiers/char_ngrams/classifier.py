import numpy as np
import datetime
import globals

from . import vector_handler

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def char_ngrams_classifier(generate_vectors, in_out_domain, vector_type, database_dir = None, clf_iterations = None):
    """
    main function for classifier, manages the process
    :param generate_vectors: boolean value, True to generate vectors, False to use ready vectors
    :param database_dir: directory of the database to generate vectors from
    :return: nothing, prints the result to the command line
    """
    print("[", datetime.datetime.now()-globals.start_time, "] initiating char_ngram classifier")
    if generate_vectors:
        if database_dir != None:
            if in_out_domain == "in":
                users_vector, \
                countries_vector \
                    = vector_handler.trichars_vector_generator(database_dir, in_out_domain, vector_type, True)

            elif in_out_domain == "out":  # you can only run out of domain classifications after you ran in domain
                users_vector, countries_vector \
                    = vector_handler.vector_loader("in", vector_type)

                out_users_vector, out_binary_countries_vector \
                    = vector_handler.trichars_vector_generator(database_dir, in_out_domain, vector_type, True)
        else:
            raise NameError('Database directory not specified')

    else:  # use the ready vectors from the vectors directory
        try:
            if in_out_domain == "in":
                users_vector, countries_vector = \
                    vector_handler.vector_loader("in", vector_type)

            elif in_out_domain == "out":
                users_vector, countries_vector, \
                out_users_vector, out_binary_countries_vector \
                    = vector_handler.vector_loader("out", vector_type)
        except NameError:
            print('Cannot load vectors from classifier')
            return

    # MOTIVATION: Once initiated, start lr_classifier immediately
    if in_out_domain == "in":
        print ("[",datetime.datetime.now()-globals.start_time, "]In-Domain classification score: ",
               logistic_regression_classifier_in(users_vector, countries_vector, vector_type, iterations_limit=clf_iterations))
    elif in_out_domain == "out":
        print("[", datetime.datetime.now() - globals.start_time, "]Out-Domain classification score: ",
              logistic_regression_classifier_out(training_users_vector=users_vector, training_countries_vector=countries_vector,
                                                 testing_users_vector=out_users_vector, testing_countries_vector=out_binary_countries_vector,
                                                 vector_type = vector_type, iterations_limit=clf_iterations))
# MOTIVATION: Family Classification

# MOTIVATION: Language Classification

def logistic_regression_classifier_in(users_vector, countries_vector, vector_type, iterations_limit = 10000):
    """
    :param users_vector: vector of vectors for each user, containing the 1000 most frequent trichars
    :param binary_countries_vector: vector of integers, containing a matching binary/family/language for each user
    :param iterations_limit: limits the iteration of each cross validation score, make it high enough to avoid warnings
    :return: Logistic Regression classification score in 10-fold (value between 0 and 1)
    """
    if iterations_limit is None:
        iterations_limit = 2000
    if vector_type == "binary":
        clf = LogisticRegression(solver='liblinear', max_iter=iterations_limit, n_jobs=-1)
    elif vector_type in {"family","language"}:
        clf = LogisticRegression(solver='lbfgs', max_iter=iterations_limit, multi_class='multinomial', n_jobs=-1)
    print("[",datetime.datetime.now()-globals.start_time, "] (in) starting cross validation process")
    print (len(users_vector))
    print(len(countries_vector))
    print(iterations_limit)
    classifier_scores = cross_val_score(clf, users_vector, countries_vector, cv=10)
    return np.average(classifier_scores)


def logistic_regression_classifier_out(training_users_vector, training_countries_vector,
                                       testing_users_vector, testing_countries_vector,
                                       iterations_limit = 20000):
    if iterations_limit is None:
        iterations_limit = 2000
    clf = LogisticRegression(solver='auto', max_iter=iterations_limit, n_jobs=-1).fit(training_users_vector, training_countries_vector)
    print("[",datetime.datetime.now()-globals.start_time, "] starting prediction process")
    return clf.score(testing_users_vector, testing_countries_vector)