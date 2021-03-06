from utilities.logger import log
import utilities.interpreter as setup
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


def classify(users, countries, train_users=None, train_countries=None):
    log('Starting classification process')
    if setup.type == 'binary':
        clf = LogisticRegression(solver='saga',
                                 max_iter=setup.iterations,
                                 n_jobs=setup.threads,
                                 class_weight='balanced')
    elif setup.type in ['family', 'language']:
        clf = LogisticRegression(solver='lbfgs',
                                 max_iter=setup.iterations,
                                 multi_class='ovr',
                                 n_jobs=setup.threads,
                                 class_weight='balanced')

    if setup.domain == 'in':
        log('Starting 10-fold cross validation process')
        classifier_scores = cross_val_score(clf, users, countries, cv=10)
        score = np.average(classifier_scores)

    elif setup.domain == 'out':
        log('Starting fit&score process')
        clf_trained = clf.fit(train_users, train_countries)
        score = clf_trained.score(users, countries)

    return score