from logger import log
import interpreter as i
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


def classify(users, countries, train_users=None, train_countries=None):
    log('Starting classification process')
    if i.type == 'binary':
        clf = LogisticRegression(solver='saga',
                                 max_iter=i.iterations,
                                 n_jobs=i.threads,
                                 class_weight='balanced')
    elif i.type in ['family', 'language']:
        clf = LogisticRegression(solver='lbfgs',
                                 max_iter=i.iterations,
                                 multi_class='ovr',
                                 n_jobs=i.threads,
                                 class_weight='balanced')

    if i.domain == 'in':
        log('Starting 10-fold cross validation process')
        classifier_scores = cross_val_score(clf, users, countries, cv=10)
        score = np.average(classifier_scores)

    elif i.domain == 'out':
        log('Starting fit&score process')
        clf_trained = clf.fit(train_users, train_countries)
        score = clf_trained.score(users, countries)

    return score